from pathlib import Path
from app.sequence_extract import find_sequence
from app.bench_extract import extract_bench_info

PDF_DIR = Path("benches")

def find_listing(case_number):
    results = []

    for pdf in PDF_DIR.glob("*.pdf"):
        seq = find_sequence(pdf, case_number)
        if seq:
            bench = extract_bench_info(pdf)
            results.append({
                "file": pdf.name,
                "sequence": seq["sequence"],
                "line": seq["line"],
                "bench": bench
            })

    return results
