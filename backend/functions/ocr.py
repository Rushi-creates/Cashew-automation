# from PIL import Image
# import pytesseract

# def extract_text_from_image(image_path: str) -> str:
#     return pytesseract.image_to_string(Image.open(image_path))

import easyocr

# Create the OCR reader only once
reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(image_path: str) -> str:
    results = reader.readtext(image_path)
    return "\n".join([text for _, text, _ in results])
