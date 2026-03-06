import json
import datetime
from pathlib import Path

DATA = Path("data")

def load_cases():

    today = datetime.date.today()

    fname = DATA / f"cases_{today}.json"

    if not fname.exists():
        print("Run notifier first")
        return []

    return json.loads(fname.read_text())

def tomorrow_cases():

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    cases = load_cases()

    results = []

    for c in cases:

        next_date = c.get("next_date","")

        if str(tomorrow.day) in next_date:
            results.append(c)

    return results

def build_digest(cases):

    text = "⚖️ Virtual Clerk — Tomorrow's Matters\n\n"

    for i,c in enumerate(cases,1):

        text += f"{i}. {c.get('case_no','')}\n"
        text += f"Bench: {c.get('bench','')}\n"
        text += f"Next: {c.get('next_date','')}\n\n"

    return text

if __name__ == "__main__":

    cases = tomorrow_cases()

    if not cases:
        print("No matters tomorrow")
    else:
        print(build_digest(cases))

