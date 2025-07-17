import os
import discord
from discord.ext import commands
from PIL import Image
import pytesseract
from credentials import DISCORD_BOT_TOKEN

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True  # Needed for Discord >=2.0
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

IMAGE_DIR = 'images'
os.makedirs(IMAGE_DIR, exist_ok=True)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.event
async def on_message(message):
    # Avoid responding to bot messages
    if message.author.bot:
        return

    # Process only messages with attachments (images)
    images = [a for a in message.attachments if a.filename.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if images:
        for attachment in images:
            file_path = os.path.join(IMAGE_DIR, attachment.filename)
            await attachment.save(file_path)
            print(f"Saved image: {file_path}")

            # Open image and run OCR
            text = pytesseract.image_to_string(Image.open(file_path))
            print(f"OCR Result for {attachment.filename}:\n{text}\n{'-'*40}")

    await bot.process_commands(message)

# Replace YOUR_BOT_TOKEN here with your Discord Bot Token
bot.run(DISCORD_BOT_TOKEN)

