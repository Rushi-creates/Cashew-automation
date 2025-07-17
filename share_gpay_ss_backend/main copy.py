# import os
# import io
# import json
# import asyncio
# import re
# from typing import List, Dict, Any

# import discord
# from PIL import Image
# import pytesseract
# import requests

# import torch
# from transformers import GPT2LMHeadModel, GPT2Tokenizer

# # =========================
# # Config / Secrets via ENV
# # =========================
# CASHEW_ENDPOINT = os.getenv("CASHEW_API_URL")
# CASHEW_TOKEN = os.getenv("CASHEW_API_TOKEN")
# DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# # =========================
# # Local GPT‑2 setup (free)
# # =========================
# model_name = "gpt2"
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)
# model = GPT2LMHeadModel.from_pretrained(model_name)
# model.eval()

# def generate_response(prompt: str, max_length: int = 150) -> str:
#     """Generate text completion using local GPT‑2."""
#     input_ids = tokenizer.encode(prompt, return_tensors="pt")
#     with torch.no_grad():
#         output = model.generate(
#             input_ids,
#             max_length=max_length,
#             num_return_sequences=1,
#             pad_token_id=tokenizer.eos_token_id,
#             temperature=0.0,
#         )
#     return tokenizer.decode(output[0], skip_special_tokens=True)

# # =========================
# # Discord client
# # =========================
# intents = discord.Intents.default()
# intents.message_content = True
# client = discord.Client(intents=intents)

# # =========================
# # OCR helper
# # =========================

# def ocr_images(attachments: List[discord.Attachment]) -> str:
#     """Run Tesseract OCR on all image attachments and concatenate text."""
#     texts: List[str] = []
#     for attachment in attachments:
#         if attachment.content_type and attachment.content_type.startswith("image"):
#             data = asyncio.run_coroutine_threadsafe(attachment.read(), client.loop).result()
#             image = Image.open(io.BytesIO(data))
#             texts.append(pytesseract.image_to_string(image))
#     return "\n".join(texts)

# # =========================
# # Receipt parsing via GPT‑2
# # =========================

# def parse_receipt(text: str) -> Dict[str, Any]:
#     """Use GPT‑2 to extract amount, date, sender, and note into JSON."""
#     prompt = (
#         "Extract the following fields from the text of a payment receipt: amount (numeric), date (YYYY-MM-DD), "
#         "sender, note. Return exactly a JSON object with keys amount, date, sender, note. If any field is missing, "
#         "use null.\nTEXT:\n" + text + "\nJSON:\n"
#     )

#     raw = generate_response(prompt)

#     # Attempt to locate the first JSON object in the model output
#     match = re.search(r"\{[^}]*\}", raw)
#     if not match:
#         return {}
#     try:
#         return json.loads(match.group(0))
#     except json.JSONDecodeError:
#         return {}

# # =========================
# # Cashew API helper
# # =========================

# def send_to_cashew(payload: Dict[str, Any]) -> None:
#     headers = {
#         "Authorization": f"Bearer {CASHEW_TOKEN}",
#         "Content-Type": "application/json",
#     }
#     requests.post(CASHEW_ENDPOINT, headers=headers, json=payload, timeout=10)

# # =========================
# # Discord event handlers
# # =========================
# @client.event
# async def on_ready():
#     print(f"Logged in as {client.user}")

# @client.event
# async def on_message(message: discord.Message):
#     if message.author.bot or not message.attachments:
#         return

#     loop = asyncio.get_running_loop()
#     text = await loop.run_in_executor(None, ocr_images, message.attachments)

#     if not text.strip():
#         await message.channel.send("❌ Unable to extract text from image(s).")
#         return

#     data = await loop.run_in_executor(None, parse_receipt, text)

#     if data:
#         await loop.run_in_executor(None, send_to_cashew, data)
#         await message.channel.send("✅ Receipt processed and sent to Cashew.")
#     else:
#         await message.channel.send("❌ Could not parse receipt.")

# # =========================
# # Entry point
# # =========================
# if __name__ == "__main__":
#     if not DISCORD_BOT_TOKEN:
#         raise RuntimeError("DISCORD_BOT_TOKEN env var not set")
#     client.run(DISCORD_BOT_TOKEN)
