from pathlib import Path
import pdfplumber

ORDERS = Path("orders")
ORDERS.mkdir(exist_ok=True)

def list_orders():
    return [f.name for f in ORDERS.glob("*")]

def extract_text(file):
    text = ""
    with pdfplumber.open(ORDERS / file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text[:4000]
