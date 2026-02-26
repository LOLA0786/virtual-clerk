import requests
from pathlib import Path

SAVE = Path("benches")
SAVE.mkdir(exist_ok=True)

# direct known cause list PDFs
URLS = [
    "https://bombayhighcourt.nic.in/data/cause_list/2026/02/27/01.pdf",
    "https://bombayhighcourt.nic.in/data/cause_list/2026/02/27/02.pdf",
    "https://bombayhighcourt.nic.in/data/cause_list/2026/02/27/03.pdf",
]

def fetch_bench_pdfs():
    downloaded = 0

    for url in URLS:
        try:
            name = url.split("/")[-1]
            path = SAVE / name

            r = requests.get(url, timeout=20)

            if r.status_code == 200 and r.headers.get("content-type","").startswith("application/pdf"):
                path.write_bytes(r.content)
                downloaded += 1
                print("Downloaded:", name)

        except:
            pass

    if downloaded == 0:
        print("⚠ No PDFs downloaded")
