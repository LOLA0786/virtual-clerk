import requests
from bs4 import BeautifulSoup
import re

def fetch_bombay_case(case_type, case_no, year):
    session = requests.Session()
    url = "https://services.ecourts.gov.in/ecourtindia_v6/"

    params = {
        "state_code": "27",
        "dist_code": "1",
        "court_code": "1",
        "case_type": case_type,
        "case_no": case_no,
        "case_year": year,
    }

    r = session.get(url, params=params, timeout=20)
    soup = BeautifulSoup(r.text, "lxml")
    text = soup.get_text(" ", strip=True)

    # extract next hearing date
    date_match = re.search(r"\d{2}-\d{2}-\d{4}", text)

    return {
        "next_date": date_match.group(0) if date_match else "Not found",
        "raw": text[:500]
    }

if __name__ == "__main__":
    print(fetch_bombay_case("WP","1234","2024"))
