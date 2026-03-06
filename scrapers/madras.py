from bs4 import BeautifulSoup
from .base_scraper import safe_get

MADRAS_CAUSE = "https://www.hcmadras.tn.gov.in/cause_list_mhc.php"

def scrape_madras():

    resp = safe_get(MADRAS_CAUSE)

    if not resp:
        return []

    soup = BeautifulSoup(resp.text,"html.parser")

    changes = []

    for a in soup.find_all("a"):

        text = a.text.strip()

        if "cause" in text.lower():

            changes.append({
                "title": text,
                "url": a.get("href","")
            })

    return changes[:20]
