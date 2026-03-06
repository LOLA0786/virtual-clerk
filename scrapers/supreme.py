from bs4 import BeautifulSoup
from .base_scraper import safe_get

SUPREME_CAUSE = "https://www.sci.gov.in/cause-list/"

def scrape_supreme():

    resp = safe_get(SUPREME_CAUSE)

    if not resp:
        return []

    soup = BeautifulSoup(resp.text,"html.parser")

    cases = []

    for link in soup.find_all("a"):

        text = link.text.strip()

        if "Bench" in text or "Item" in text:

            cases.append({
                "case": text,
                "next_date": "today",
                "bench": "Supreme Court"
            })

    return cases[:50]
