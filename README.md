# Discord Video Downloader Bot

A lightweight and efficient Discord bot built with `discord.py` to download videos from various platforms and share them directly or via cloud links.

## Features

* **Video Download:** Download videos using URL inputs through Discord slash commands.
* **Smart Sharing:** 
  * Automatically attaches videos directly to Discord if under 24MB.
  * Automatically uploads videos to Litterbox (stored for 72 hours) if they exceed the Discord file limit (up to 1GB).
* **Asynchronous Uploads:** Built entirely using async libraries to prevent the bot from lagging during large transfers.

## Installation & Prerequisites

### 1. Install System Dependencies

Before installing the Python packages, you must install Python and FFmpeg on your system. **FFmpeg is strictly required** by `yt-dlp` to merge high-quality video and audio tracks together.

#### For Termux (Android)
```bash
pkg update && pkg upgrade -y
pkg install python ffmpeg git -y
```

#### For Linux (Ubuntu/Debian)
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip ffmpeg git -y
```

#### For Windows
1. Download and install [Python](https://python.org). Ensure you check the box **"Add Python to PATH"** during setup.
2. Download [FFmpeg](https://ffmpeg.org) and add its `bin` folder to your system's Environment Variables (PATH).

### 2. Install Python Requirements

Clone this repository, navigate to the project folder, and run the following command to automatically install all required Python modules listed in your requirements file:

```bash
pip install -r requirements.txt
```

## Configuration

Set up your Discord bot token as an environment variable:

```bash
nano .env
DISCORD_TOKEN="YOUR_BOT_TOKEN_HERE"
```

## Running the Bot

Start the bot script by executing:

```bash
python bot.py
```

## Usage

Once the bot is online, use the slash command in your Discord server:

```text
/download [url]
```

* **Example:** `/download url:https://youtube.com`
