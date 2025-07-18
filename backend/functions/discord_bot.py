import os
import discord
from discord.ext import commands
from functions.gpt_layer import generate_response
from functions.ocr import print_ocrspace_text
from utils.prompt import prompt_template
from utils.credentials import DISCORD_BOT_TOKEN


IMAGE_DIR = 'images'
os.makedirs(IMAGE_DIR, exist_ok=True)

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'🤖 Bot connected as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    images = [a for a in message.attachments if a.filename.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if images:
        for attachment in images:
            file_path = os.path.join(IMAGE_DIR, attachment.filename)
            await attachment.save(file_path)
            print(f"📥 Saved image: {file_path}")

            print_ocrspace_text(file_path)


    await bot.process_commands(message)

def start_discord_bot():
    bot.run(DISCORD_BOT_TOKEN)
