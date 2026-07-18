import subprocess
import time
def start_server():
    subprocess.Popen(["python", "server.py"])
    print("Server is starting...")
    time.sleep(2)
    print("Server should be running now!")

def start_bot():
    print("Starting the bot...")
    subprocess.run(["python", "rpc.py"])

if __name__ == "__main__":
    start_server()
    start_bot()
