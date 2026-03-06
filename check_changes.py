import json
from pathlib import Path
import datetime

from change_detector import detect_hearing_changes
from hearing_alerts import print_hearing_changes

DATA = Path("data")

today = datetime.date.today()

today_file = DATA / f"cases_{today}.json"

if not today_file.exists():

    print("No snapshot found for today. Run notifier first.")
    exit()

today_cases = json.loads(today_file.read_text())

changes = detect_hearing_changes(today_cases)

print_hearing_changes(changes)
