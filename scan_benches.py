import pdfplumber
from pathlib import Path

CASE_NUMBER = "1234"

def scan_pdf(file):
    try:
        with pdfplumber.open(file) as pdf:
            for page_no, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""

                if CASE_NUMBER in text:
                    print(f"\n✅ FOUND in {file}")
                    print(f"Page: {page_no}")
                    print(text[:300])
                    return True
    except Exception as e:
        print(f"Skipping {file} (not valid PDF)")
    return False

pdfs = Path(".").glob("*.pdf")

found = False
for pdf in pdfs:
    if scan_pdf(pdf):
        found = True

if not found:
    print("\n❌ Case not listed today")
