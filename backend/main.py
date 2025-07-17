import os
import discord
from discord.ext import commands
from PIL import Image
import pytesseract

import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

from credentials import DISCORD_BOT_TOKEN  # Add your SECRET token in this file
from prompt import prompt_template

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True  # Needed for Discord >=2.0
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

IMAGE_DIR = 'images'
os.makedirs(IMAGE_DIR, exist_ok=True)


# GPT-2 model
model_name = "gpt2"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
model.eval()

def generate_response(prompt: str, max_new_tokens: int = 120) -> str:
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,   # Specify output tokens directly
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id,
        )
    return tokenizer.decode(output[0], skip_special_tokens=True)



# OCR

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Process attached images only
    images = [a for a in message.attachments if a.filename.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if images:
        for attachment in images:
            file_path = os.path.join(IMAGE_DIR, attachment.filename)
            await attachment.save(file_path)
            print(f"Saved image: {file_path}")

            # OCR extraction
            text = pytesseract.image_to_string(Image.open(file_path))
            print(f"OCR Result for {attachment.filename}:\n{text}\n{'-'*40}")

            # Prepare prompt for GPT-2
            prompt = prompt_template.format(ocr_text=text)
            gpt2_response = generate_response(prompt)

            print("GPT-2 extracted transaction details:")
            print(gpt2_response)

            response_text = gpt2_response.split('Transaction Details:')[-1]

            print("\n🧾 Parsed Transaction Details:")
            for line in response_text.strip().splitlines():
                line = line.strip()
                if line and ':' in line:
                    key, value = line.split(':', 1)
                    print(f"{key.strip()}: {value.strip()}")
                elif line:
                    print(f"- {line.strip()}")  # catch extra bullet lines


    await bot.process_commands(message)

# Replace YOUR_BOT_TOKEN here with your Discord Bot Token
bot.run(DISCORD_BOT_TOKEN)

