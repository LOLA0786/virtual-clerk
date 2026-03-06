import time
import json
from pathlib import Path

DATA = Path("data")
LAWYERS = DATA / "lawyers.json"

def load_lawyers():

    if not LAWYERS.exists():
        return []

    return json.loads(LAWYERS.read_text())

def run():

    while True:

        lawyers = load_lawyers()

        for l in lawyers:

            for adv in l["advocates"]:

                print("Checking advocate:",adv)

                # here plug your search_advocate()
                # or notifier logic

        print("sleeping 10 minutes")

        time.sleep(600)

if __name__=="__main__":
    run()
