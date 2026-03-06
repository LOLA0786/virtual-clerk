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

from bs4 import BeautifulSoup

def extract_case_info_from_html(html):
    """
    Extract next hearing date, stage, and judge from Bombay HC case HTML.
    """

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    data = {
        "next_hearing": None,
        "stage": None,
        "judge": None
    }

    # Next Hearing Date
    if "Next Hearing Date" in text:
        try:
            part = text.split("Next Hearing Date")[1]
            date = part.split(":")[1].strip().split(" ")
            data["next_hearing"] = " ".join(date[:3])
        except Exception:
            pass

    # Stage
    if "Stage of Case" in text:
        try:
            part = text.split("Stage of Case")[1]
            data["stage"] = part.split(":")[1].strip()
        except Exception:
            pass

    # Judge (Coram)
    if "Coram" in text:
        try:
            part = text.split("Coram")[1]
            data["judge"] = part.split(":")[1].strip()
        except Exception:
            pass

    return data


import re
from bs4 import BeautifulSoup

def extract_case_info_from_html(html):
    """
    Extract next hearing date, stage, and judge from Bombay HC HTML.
    Uses regex to avoid grabbing extra labels.
    """

    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)

    data = {
        "next_hearing": None,
        "stage": None,
        "judge": None
    }

    # Next Hearing Date
    m = re.search(r"Next Hearing Date\s*:\s*([0-9a-zA-Z\s]+)", text)
    if m:
        data["next_hearing"] = m.group(1).strip()

    # Stage
    m = re.search(r"Stage of Case\s*:\s*([A-Z\s\(\)]+)", text)
    if m:
        data["stage"] = m.group(1).strip()

    # Judge
    m = re.search(r"Coram\s*:\s*([A-Z' \.\-]+JUSTICE[ A-Z\.\-']+)", text)
    if m:
        judge = m.group(1).strip()
        judge = re.sub(r'^\d+', '', judge)  # remove numeric prefix
        data["judge"] = judge

    return data


from bs4 import BeautifulSoup

def extract_case_info_from_html(html):
    """
    Extract case info from Bombay HC case details HTML.
    Uses label matching instead of regex.
    """

    soup = BeautifulSoup(html, "html.parser")

    data = {
        "next_hearing": None,
        "stage": None,
        "judge": None
    }

    labels = soup.find_all("strong")

    for i, label in enumerate(labels):

        text = label.get_text(strip=True)

        if "Next Hearing Date" in text:
            if i + 1 < len(labels):
                data["next_hearing"] = labels[i+1].get_text(strip=True)

        if "Stage of Case" in text:
            if i + 1 < len(labels):
                data["stage"] = labels[i+1].get_text(strip=True)

        if "Coram" in text:
            if i + 1 < len(labels):
                judge = labels[i+1].get_text(strip=True)
                judge = ''.join(c for c in judge if not c.isdigit())
                data["judge"] = judge.strip()

    return data


from bs4 import BeautifulSoup

def clean_value(v):
    if not v:
        return None
    v = v.replace(":", "")
    v = v.replace("\xa0", " ")
    return v.strip()

def extract_case_info_from_html(html):

    soup = BeautifulSoup(html, "html.parser")

    data = {
        "next_hearing": None,
        "stage": None,
        "judge": None
    }

    labels = soup.find_all("strong")

    for i, label in enumerate(labels):

        text = label.get_text(strip=True)

        if "Next Hearing Date" in text:
            if i + 1 < len(labels):
                data["next_hearing"] = clean_value(
                    labels[i+1].get_text()
                )

        if "Stage of Case" in text:
            if i + 1 < len(labels):
                data["stage"] = clean_value(
                    labels[i+1].get_text()
                )

        if "Coram" in text:
            if i + 1 < len(labels):
                judge = clean_value(labels[i+1].get_text())
                judge = ''.join(c for c in judge if not c.isdigit())
                data["judge"] = judge

    return data

