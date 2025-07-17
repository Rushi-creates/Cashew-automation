from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pytesseract
from PIL import Image
import tempfile
import requests

app = FastAPI()

CASHEW_API = "https://cashew.app/api/transactions"  # Replace with real

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        img = Image.open(tmp_path)
        text = pytesseract.image_to_string(img)

        parsed = extract_transaction_info(text)

        # Send to Cashew
        cashew_response = requests.post(CASHEW_API, json=parsed)

        return {
            "status": "ok",
            "ocr_text": text,
            "parsed": parsed,
            "cashew_status": cashew_response.status_code
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

def extract_transaction_info(text):
    lines = text.splitlines()
    info = {
        "amount": None,
        "upi_id": None,
        "timestamp": None,
        "sender": None
    }

    for line in lines:
        if "Rs" in line or "₹" in line:
            info["amount"] = line.strip()
        if "@upi" in line:
            info["upi_id"] = line.strip()
        if ":" in line and any(w in line.lower() for w in ["am", "pm"]):
            info["timestamp"] = line.strip()
        if "to" in line.lower() or "from" in line.lower():
            info["sender"] = line.strip()

    return info
