import os
import discord
from discord.ext import commands
import yt_dlp
import aiohttp
import aiofiles
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"Downloading: {d.get('_percent_str', 'N/A')}", end='', flush=True)
    elif d['status'] == 'finished':
        print("\nDownload complete, processing...")

async def upload_file(filename):
    url = "https://catbox.moe/user/api.php"
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('reqtype', 'fileupload')
        data.add_field('file', open(filename, 'rb'), filename=os.path.basename(filename))
        
        try:
            async with session.post(url, data=data, timeout=120) as resp:
                if resp.status == 200:
                    return await resp.text()
        except Exception as e:
            print(f"\nUpload Error: {e}")
    return None

@bot.tree.command(name="download", description="Download video")
async def download(interaction: discord.Interaction, url: str):
    await interaction.response.send_message("Processing...", ephemeral=True)
    
    filename = 'downloaded_video.mp4'

    if os.path.exists(filename):
        os.remove(filename)

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': filename,
        'cookiefile': 'cookies.txt',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'skip_postprocessors': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        size = os.path.getsize(filename) / (1024 * 1024)

        if size <= 24:
            await interaction.followup.send("Here is the video:", file=discord.File(filename), ephemeral=True)
        else:
            await interaction.followup.send("File is too large, uploading to Catbox.moe...", ephemeral=True)
            link = await upload_file(filename)
            
            if link and link.startswith("http") and len(link.strip()) < 200:
                await interaction.followup.send(f"Link: {link.strip()}", ephemeral=True)
            else:
                await interaction.followup.send("❌ Upload failed or Catbox returned an invalid link.", ephemeral=True)

        if os.path.exists(filename):
            os.remove(filename)

    except Exception as e:
            await interaction.followup.send(f"Error: {e}", ephemeral=True)
            if os.path.exists(filename):
                os.remove(filename)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

bot.run(os.getenv('DISCORD_TOKEN'))
