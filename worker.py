import time
from models import SessionLocal, Advocate
from bombay_hc import fetch_bombay_case

while True:

    db = SessionLocal()

    advocates = db.query(Advocate).all()

    for a in advocates:

        print("Checking:", a.advocate_name)

        # call your scraper
        # replace with your search_advocate function

    print("Sleeping...")

    time.sleep(1800)
