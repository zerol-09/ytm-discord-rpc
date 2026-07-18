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
    └── launcher.py
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

### Python Backend

Install required packages:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
python launcher.py
```

Open YouTube Music and start playing a song.

## Requirements

* Google Chrome
* Python 3.11
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
