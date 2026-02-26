import pdfplumber
import re

def find_sequence(file, case_number):
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""

            for line in text.split("\n"):
                if case_number in line:
                    match = re.match(r'\s*(\d+)', line)
                    if match:
                        return {
                            "sequence": match.group(1),
                            "line": line.strip()
                        }
    return None
