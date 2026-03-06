import json
import datetime
from pathlib import Path

DATA = Path("data")

def detect_hearing_changes(today_cases):

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    old_file = DATA / f"cases_{yesterday}.json"

    if not old_file.exists():
        print("No previous snapshot found")
        return []

    old_cases = json.loads(old_file.read_text())

    old_map = {c["case_no"]: c for c in old_cases}

    changes = []

    for c in today_cases:

        case_no = c["case_no"]
        new_date = c.get("next_hearing")

        if case_no in old_map:

            old_date = old_map[case_no].get("next_hearing")

            if old_date and new_date and old_date != new_date:

                changes.append({
                    "case_no": case_no,
                    "old_date": old_date,
                    "new_date": new_date,
                    "bench": c.get("bench","")
                })

    return changes
