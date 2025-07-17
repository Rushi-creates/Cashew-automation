import os
import discord
from discord.ext import commands
from functions.gpt_layer import generate_response
from functions.ocr import extract_text_from_image
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

            text = extract_text_from_image(file_path)
            print(f"\n🧾 OCR Result:\n{text}\n{'-'*40}")

            prompt = prompt_template.format(ocr_text=text)
            gpt2_response = generate_response(prompt)

            print("🧠 GPT-2 extracted transaction details:")
            print(gpt2_response)

            response_text = gpt2_response.split('Transaction Details:')[-1]

            print("\n✅ Parsed Transaction Details:")
            for line in response_text.strip().splitlines():
                line = line.strip()
                if line and ':' in line:
                    key, value = line.split(':', 1)
                    print(f"{key.strip()}: {value.strip()}")
                elif line:
                    print(f"- {line.strip()}")

    await bot.process_commands(message)

def start_discord_bot():
    bot.run(DISCORD_BOT_TOKEN)
