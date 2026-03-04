import requests
import pdfplumber
from pathlib import Path

URL = "https://bombayhighcourt.nic.in/causelist/cause_list.pdf"
PDF_FILE = Path("cause_list.pdf")


def download_cause_list():
    print("Downloading cause list...")
    r = requests.get(URL, timeout=30)
    PDF_FILE.write_bytes(r.content)
    print("Saved cause_list.pdf")


def search_case(case_number):
    with pdfplumber.open(PDF_FILE) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()

            if case_number in text:
                return page_number, text

    return None, None


if __name__ == "__main__":
    download_cause_list()
    page, text = search_case("WP-1234-2024")

    if page:
        print(f"Found on page {page}")
    else:
        print("Case not listed")
