import json
import datetime
from pathlib import Path
from collections import defaultdict

# --- simple date normalizer ---
import re
from datetime import datetime as dt

def normalize_date(date_str):
    if not date_str:
        return None
    s = date_str.strip()
    s = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', s)  # 04th -> 04
    fmts = ["%d %B %Y", "%d %b %Y", "%d-%m-%Y", "%d/%m/%Y"]
    for f in fmts:
        try:
            return dt.strptime(s, f).strftime("%Y-%m-%d")
        except:
            pass
    return None

DATA = Path("data")

files = sorted(DATA.glob("cases_*.json"))
if not files:
    print("No snapshots found. Run notifier_v2.py first.")
    exit()

latest = files[-1]
cases = json.loads(latest.read_text())

today = datetime.date.today().strftime("%Y-%m-%d")

today_cases = []

for c in cases:
    d = normalize_date(c.get("next_hearing"))
    if d == today:
        today_cases.append(c)

if not today_cases:
    print("⚖ No tracked matters listed today.")
    exit()

# group by bench
by_bench = defaultdict(list)
for c in today_cases:
    bench = c.get("bench") or c.get("judge") or "Unknown Bench"
    by_bench[bench].append(c)

print(f"\n⚖ Virtual Clerk – Your Matters Today ({today})\n")

for bench in sorted(by_bench.keys()):
    print(f"Bench: {bench}")
    for c in by_bench[bench]:
        case_no = c.get("case_no","?")
        pet = c.get("petitioner","")[:50]
        res = c.get("respondent","")[:50]
        print(f"  - {case_no} | {pet} vs {res}")
    print()

