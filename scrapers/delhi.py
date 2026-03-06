from bs4 import BeautifulSoup
from .base_scraper import safe_get

DELHI_CAUSE_URL = "https://delhihighcourt.nic.in/"

def scrape_delhi(keyword):

    resp = safe_get(DELHI_CAUSE_URL)

    if not resp:
        return []

    soup = BeautifulSoup(resp.text,"html.parser")

    cases = []

    tables = soup.find_all("table")

    for table in tables:

        rows = table.find_all("tr")

        for row in rows:

            cols = row.find_all("td")

            if len(cols) >= 4:

                case = {
                    "case_no": cols[0].text.strip(),
                    "parties": cols[1].text.strip(),
                    "next_date": cols[2].text.strip(),
                    "bench": cols[3].text.strip()
                }

                if keyword.lower() in str(case).lower():
                    cases.append(case)

    return cases
