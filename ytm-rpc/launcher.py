import atexit
import ctypes
import subprocess
import sys
import time
from pathlib import Path

import psutil


DISCORD_PROCESSES = {
    "discord.exe",
    "discordcanary.exe",
    "discordptb.exe",
}

CHILD_PROGRAMS = [
    "server.exe",
    "rpc.exe",
]

CHECK_INTERVAL = 2

children: list[subprocess.Popen] = []


def prevent_duplicate_launcher() -> None:

    mutex_name = "YTMDiscordRPCLauncherMutex"

    mutex = ctypes.windll.kernel32.CreateMutexW(
        None,
        False,
        mutex_name,
    )

    already_exists = ctypes.windll.kernel32.GetLastError() == 183

    if already_exists:
        sys.exit(0)


    global launcher_mutex
    launcher_mutex = mutex


def get_app_folder() -> Path:

    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent


def is_discord_running() -> bool:

    for process in psutil.process_iter(["name"]):
        try:
            process_name = process.info["name"]

            if (
                process_name
                and process_name.lower() in DISCORD_PROCESSES
            ):
                return True

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess,
        ):
            continue

    return False


def start_children() -> None:
    global children

    app_folder = get_app_folder()
    children = []

    server_path = app_folder / "server.exe"
    rpc_path = app_folder / "rpc.exe"

    try:
        server_process = subprocess.Popen(
            [str(server_path)],
            cwd=str(app_folder),
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

        children.append(server_process)
        write_log(f"Started server.exe, PID {server_process.pid}")

        time.sleep(3)

        rpc_process = subprocess.Popen(
            [str(rpc_path)],
            cwd=str(app_folder),
            creationflags=subprocess.CREATE_NO_WINDOW,
        )

        children.append(rpc_process)
        write_log(f"Started rpc.exe, PID {rpc_process.pid}")

    except OSError as error:
        write_log(f"Failed to start child program: {error}")


def stop_process_tree(process: subprocess.Popen) -> None:

    try:
        parent = psutil.Process(process.pid)
    except psutil.NoSuchProcess:
        return

    descendants = parent.children(recursive=True)

    for child in descendants:
        try:
            child.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    try:
        parent.terminate()
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        pass

    processes = descendants + [parent]

    _, still_alive = psutil.wait_procs(processes, timeout=5)

    for remaining_process in still_alive:
        try:
            remaining_process.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


def stop_children() -> None:
    global children

    for process in children:
        stop_process_tree(process)

    children = []
    write_log("Stopped child programs")


def restart_crashed_children() -> None:

    if not children:
        start_children()
        return

    if any(process.poll() is not None for process in children):
        write_log("A child program closed unexpectedly; restarting")
        stop_children()
        start_children()


def write_log(message: str) -> None:
    app_folder = get_app_folder()
    log_file = app_folder / "launcher.log"

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    try:
        with log_file.open("a", encoding="utf-8") as file:
            file.write(f"[{timestamp}] {message}\n")
    except OSError:
        pass


def main() -> None:
    prevent_duplicate_launcher()
    atexit.register(stop_children)

    discord_was_running = False

    write_log("Launcher started")

    while True:
        discord_is_running = is_discord_running()

        if discord_is_running and not discord_was_running:
            write_log("Discord detected")
            start_children()

        elif not discord_is_running and discord_was_running:
            write_log("Discord closed")
            stop_children()

        elif discord_is_running:
            restart_crashed_children()

        discord_was_running = discord_is_running
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()