# YouTube Music Discord Rich Presence

A custom Discord Rich Presence system that displays your currently playing YouTube Music song on Discord.

This project consists of a browser extension that extracts YouTube Music playback information and a Python backend that communicates with Discord Rich Presence.

## Features

* Displays currently playing YouTube Music track on Discord
* Shows:

  * Song title
  * Artist name
  * Album artwork / thumbnail
  * Playback position and duration
  * Listening status
* Automatically updates when:

  * A new song starts
  * Playback is paused/resumed
  * The user seeks through a song
* Automatically launches the backend when Discord starts
* Automatically stops backend processes when Discord closes
* Automatically restarts backend processes if they unexpectedly crash
* Prevents duplicate launcher instances
* First-time Discord Application ID setup
* Saves user configuration automatically

## How It Works

The project is split into two parts:

### 1. YouTube Music Extension

Located in:

```
ytm-extension/
```

The browser extension runs on YouTube Music and extracts information from the player, including:

* Song title
* Artist
* Thumbnail
* Duration
* Current playback position
* Playing state

The data is then sent to the local Python server.

### 2. Discord RPC Backend

Located in:

```
ytm-rpc/
```

The Python backend:

* Receives song data from the extension
* Processes playback information
* Updates Discord Rich Presence using Discord RPC
* Automatically manages backend processes through the launcher

## Project Structure

```
ytm-discord-rpc/
│
├── ytm-extension/
│   ├── manifest.json
│   ├── content.js
│   └── injected.js
│
└── ytm-rpc/
    ├── server.py
    ├── rpc.py
    ├── launcher.py
    └── requirements.txt
```

## Installation

### Browser Extension

1. Open Chrome extensions:

```
chrome://extensions/
```

2. Enable **Developer Mode**

3. Select **Load unpacked**

4. Choose:

```
ytm-extension/
```

## Python Backend

Navigate to the backend folder:

```bash
cd ytm-rpc
```

Install required packages:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
python launcher.py
```

# Building Executables

This project uses **PyInstaller** to package the Python scripts into standalone Windows executables.

## Prerequisites

Install PyInstaller:

```bash
py -m pip install pyinstaller
```

Navigate to the folder containing the Python scripts:

```bash
cd ytm-rpc
```

## Build `rpc.exe`

```bash
py -m PyInstaller --onefile --windowed --clean --collect-all ytmusicapi --name rpc rpc.py
```

## Build `server.exe`

```bash
py -m PyInstaller --onefile --windowed --clean --name server server.py
```

## Build `launcher.exe`

```bash
py -m PyInstaller --onefile --windowed --clean --name launcher launcher.py
```

## Output

After building, the executables will be located in the `dist` folder:

```text
dist/
├── rpc.exe
├── server.exe
└── launcher.exe
```

---

## Running the Application

Alternatively, download the latest release from the **Releases** page.

1. Run `launcher.exe`.
2. On first launch, enter your Discord Application ID when prompted.
3. The application will save the ID automatically for future launches.
4. Open YouTube Music and start playing a song.

---

## Requirements

- Google Chrome
- Discord Desktop Application
- YouTube Music account

### Only required if building from source

- Python 3.11 or later
- PyInstaller

## Optional: Start Automatically with Windows

If you want the Rich Presence to start automatically whenever you log in:

1. Press **Win + R**.
2. Type `shell:startup` and press **Enter**.
3. Copy `launcher.exe` (or a shortcut to it) into the Startup folder.

The application will now launch automatically each time you sign in to Windows.
## License

This project is for educational and personal use.