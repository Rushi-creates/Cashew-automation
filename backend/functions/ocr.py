from PIL import Image
import pytesseract
import requests

def extract_text_from_image(image_path: str) -> str:
    return pytesseract.image_to_string(Image.open(image_path))

# import easyocr

# # Create the OCR reader only once
# reader = easyocr.Reader(['en'], gpu=False)

# def extract_text_from_image(image_path: str) -> str:
#     results = reader.readtext(image_path)
#     return "\n".join([text for _, text, _ in results])

import re

def extract_text_from_image_ocrspace(image_path: str, api_key: str = 'helloworld') -> str:
    """Extract text from image using OCR.Space API (free tier)."""
    payload = {
        'isOverlayRequired': False,
        'apikey': api_key,
        'language': 'eng',
    }
    with open(image_path, 'rb') as f:
        r = requests.post(
            'https://api.ocr.space/parse/image',
            files={'filename': f},
            data=payload,
        )
    result = r.json()
    if result.get('ParsedResults'):
        return result['ParsedResults'][0]['ParsedText']
    else:
        return ''

# Update parse_gpay_receipt to use OCR.Space

def parse_gpay_receipt(image_path: str, api_key: str = 'helloworld'):
    import re
    text = extract_text_from_image_ocrspace(image_path, api_key)
    lines = [line.strip() for line in text.split('\n') if line.strip()]

    sender = None
    amount = None
    note = None
    status = None
    date = None

    # 1. Sender name: usually first non-empty line after time (skip icons, time, etc.)
    for i, line in enumerate(lines):
        # Look for 'From' or 'To' pattern
        if line.lower().startswith('from '):
            sender = line[5:].strip()
            sender_idx = i
            break
    else:
        # fallback: first line with a name-like pattern
        for i, line in enumerate(lines):
            if re.match(r'^[A-Za-z ]+$', line) and len(line.split()) >= 2:
                sender = line.strip()
                sender_idx = i
                break
            
    # 2. Amount: look for line with '₹' and a number
    for i, line in enumerate(lines):
        amt_match = re.search(r'₹\s*([\d,]+\.?\d*)', line)
        if amt_match:
            amount = amt_match.group(1)
            amount_idx = i
            break

    # 3. Note: line between amount and status (optional)
    note = None
    if amount is not None:
        # Look for 'Completed' or 'Pay again' after amount
        for j in range(amount_idx+1, min(amount_idx+4, len(lines))):
            if lines[j].lower() not in ['completed', 'pay again'] and not re.match(r'\d{1,2} \w+ \d{4}', lines[j]):
                note = lines[j]
                break

    # 4. Status: look for 'Completed' or 'Pay again'
    for line in lines:
        if 'completed' in line.lower():
            status = 'Received'
            break
        elif 'pay again' in line.lower():
            status = 'Sent'
            break

    # 5. Date: look for date pattern (e.g., 12 Jul 2025, 3:02 pm)
    for line in lines:
        date_match = re.search(r'(\d{1,2} \w+ \d{4},? \d{1,2}:\d{2} ?[ap]m)', line)
        if date_match:
            date = date_match.group(1)
            break

    print(f"Sender: {sender}")
    print(f"Amount: ₹{amount}")
    print(f"Note: {note if note else '-'}")
    print(f"Status: {status}")
    print(f"Date: {date}")

# Example usage:
# parse_gpay_receipt('path/to/your/image.jpg')

def print_ocrspace_text(image_path: str, api_key: str = 'helloworld'):
    """Extract and print all text from an image using OCR.Space API, no parsing."""
    text = extract_text_from_image_ocrspace(image_path, api_key)
    print(text)
