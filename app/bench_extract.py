import pdfplumber
import re

def extract_bench_info(file):
    with pdfplumber.open(file) as pdf:
        text = pdf.pages[0].extract_text()

    lines = text.split("\n")

    info = {
        "court": "",
        "bench": [],
        "time": ""
    }

    for line in lines:

        if "COURT NO." in line:
            info["court"] = line.strip()

        if "HON'BLE" in line:
            info["bench"].append(line.strip())

        # match session start time lines like "AT 11:00 AM"
        if re.search(r'^\s*AT\s+\d{1,2}:\d{2}\s*(AM|PM)', line):
            info["time"] = line.strip()

    return info
