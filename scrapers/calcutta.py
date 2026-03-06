from bs4 import BeautifulSoup
from .base_scraper import safe_get

CALCUTTA_URL = "https://www.calcuttahighcourt.gov.in/Cause-Lists"

def scrape_calcutta():

    resp = safe_get(CALCUTTA_URL)

    if not resp:
        return []

    soup = BeautifulSoup(resp.text,"html.parser")

    updates = []

    for a in soup.find_all("a",href=True):

        href = a["href"]

        if "pdf" in href.lower():

            updates.append({
                "type":"pdf_update",
                "url":"https://www.calcuttahighcourt.gov.in"+href
            })

    return updates[:5]
