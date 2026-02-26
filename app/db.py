import json
from pathlib import Path

DATA = Path("data/cases.json")

def load():
    if not DATA.exists():
        return {}
    return json.loads(DATA.read_text())

def save(data):
    DATA.write_text(json.dumps(data, indent=2))
