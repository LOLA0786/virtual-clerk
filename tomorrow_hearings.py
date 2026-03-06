import json
import datetime
from pathlib import Path
from date_normalizer import normalize_date

DATA = Path("data")

files = sorted(DATA.glob("cases_*.json"))

if not files:
    print("No case snapshots found")
    exit()

latest = files[-1]

cases = json.loads(latest.read_text())

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

tomorrow_cases = []

for c in cases:

    date = normalize_date(c.get("next_hearing"))

    if date == tomorrow.strftime("%Y-%m-%d"):
        tomorrow_cases.append(c)

print(f"\n⚖ Hearings Tomorrow ({len(tomorrow_cases)})\n")

for c in tomorrow_cases:

    print(
        f"{c.get('case_no')} | "
        f"{c.get('bench','')} | "
        f"{c.get('next_hearing')}"
    )
