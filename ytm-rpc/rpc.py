import asyncio
import requests
from pypresence import ActivityType, AioPresence, StatusDisplayType
from ytmusicapi import YTMusic
import json
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, simpledialog

yt_music = YTMusic()

def get_app_folder() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parent


def get_config_path() -> Path:
    return get_app_folder() / "config.json"


def is_valid_application_id(application_id: str) -> bool:
    return application_id.isdigit() and 15 <= len(application_id) <= 25


def ask_for_application_id() -> str:
    root = tk.Tk()
    root.withdraw()

    while True:
        application_id = simpledialog.askstring(
            "YouTube Music Discord RPC",
            "Enter your Discord Application ID:",
            parent=root,
        )

        if application_id is None:
            root.destroy()
            raise SystemExit("Setup cancelled")

        application_id = application_id.strip()

        if is_valid_application_id(application_id):
            root.destroy()
            return application_id

        messagebox.showerror(
            "Invalid Application ID",
            "The Application ID must contain only numbers.",
            parent=root,
        )


def save_application_id(application_id: str) -> None:
    config_path = get_config_path()

    config = {
        "discord_application_id": application_id
    }

    with config_path.open("w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)


def load_application_id() -> str:
    config_path = get_config_path()

    if config_path.exists():
        try:
            with config_path.open("r", encoding="utf-8") as file:
                config = json.load(file)

            application_id = str(
                config.get("discord_application_id", "")
            ).strip()

            if is_valid_application_id(application_id):
                return application_id

        except (OSError, json.JSONDecodeError):
            pass

    application_id = ask_for_application_id()
    save_application_id(application_id)

    return application_id

CLIENT_ID = load_application_id()
rpc = AioPresence(CLIENT_ID)
is_connected = False

async def ensure_rpc_connected():
    global is_connected
    if not is_connected:
        try:
            await rpc.connect()
            is_connected = True
        except Exception as e:
            print(f"Failed to connect to Discord: {e}")
            is_connected = False

async def get_active_media_info():

    response = requests.get("http://127.0.0.1:5000/current").json()
    title = response.get("title")
    artist = response.get("artist")
    thumbnail = response.get("thumbnail")
    duration = response.get("duration")
    position = response.get("position")
    isplaying = response.get("playing")
    time = response.get("time")

    return {"title": title, "artist": artist, "thumbnail": thumbnail, "duration": duration, "position": position, "playing": isplaying, "time": time}

async def main():
    print("Listening for system audio changes and song lengths...")

    last_track = None
    last_position = -1
    drift_threshold = 2 

    while True:
        await asyncio.sleep(1)
        media_info = await get_active_media_info()

        if media_info["playing"] and media_info["title"] and media_info["artist"] and media_info["duration"] > 0:
            track_identifier = f"{media_info['title']} - {media_info['artist']}"
            current_position = media_info['position']
            track_changed = track_identifier != last_track
            time_drifted = abs((current_position-last_position) - 1) > drift_threshold if last_position >= 0 else False
            if track_changed or time_drifted:
                await ensure_rpc_connected()

                if is_connected:
                    now = media_info['time']
                    start_timestamp = now - (current_position * 1000)
                    end_timestamp = start_timestamp + (media_info['duration'] * 1000)
                    start_timestamp = int(start_timestamp / 1000)
                    end_timestamp = int(end_timestamp / 1000)
                    safe_details = media_info['title'] if len(media_info['title']) <= 128 else media_info['title'][:125] + "..."
                    artist_string = f"by {media_info['artist']}"
                    safe_state = artist_string if len(artist_string) <= 128 else artist_string[:125] + "..."
                    thumbnail_url = media_info['thumbnail'] if media_info['thumbnail'] else None
                    await rpc.update(
                        name="YouTube Music",
                        activity_type=ActivityType.LISTENING,
                        status_display_type=StatusDisplayType.DETAILS,
                        details=safe_details,
                        state=safe_state,
                        start=start_timestamp,
                        end=end_timestamp,
                        large_image=thumbnail_url,
                    )
                    
                    if track_changed:
                        mins, secs = divmod(media_info['duration'], 60)
                        print(f"Playing: {track_identifier} [{mins:02d}:{secs:02d}]")
                        last_track = track_identifier
                    
            last_position = current_position
        else:
            if last_track is not None:
                if is_connected:
                    await rpc.clear()
                print("Media stopped. Cleared Discord RPC.")
                last_track = None
                last_position = -1


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping RPC script.")
