from bs4 import BeautifulSoup
from .base_scraper import safe_get

KARNATAKA_SEARCH = "https://judiciary.karnataka.gov.in/causelistSearch.php"

def scrape_karnataka(keyword):

    params = {"keyWord": keyword}

    resp = safe_get(KARNATAKA_SEARCH,params=params)

    if not resp:
        return []

    soup = BeautifulSoup(resp.text,"html.parser")

    cases = []

    tables = soup.find_all("table")

    for table in tables:

        rows = table.find_all("tr")

        for row in rows:

            cols = row.find_all("td")

            if len(cols) >= 3:

                cases.append({
                    "case_no": cols[0].text.strip(),
                    "parties": cols[1].text.strip(),
                    "bench": cols[2].text.strip()
                })

    return cases
