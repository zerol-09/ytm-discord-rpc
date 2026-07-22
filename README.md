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

Or download the latest release from the **Releases** page and run:

```
launcher.exe
```

On first launch, the application will ask for your Discord Application ID and save it automatically for future launches.

Open YouTube Music and start playing a song.

## Requirements

* Google Chrome
* Python 3.11 (only if building from source)
* Discord Desktop Application
* YouTube Music account

## Future Improvements

Possible improvements:

* Better playback synchronization
* Improved error handling
* Easier installation process
* Support for additional music platforms

## License

This project is for educational and personal use.