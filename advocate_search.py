import requests
from bs4 import BeautifulSoup
import datetime
import subprocess
import tempfile
import cv2
import numpy as np

BASE = "https://hcservices.ecourts.gov.in/ecourtindiaHC/"

def solve_captcha(session, headers):

    captcha_url = BASE + "securimage/securimage_show.php"
    r = session.get(captcha_url, headers=headers)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        f.write(r.content)
        captcha_file = f.name

    src = cv2.imread(captcha_file)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    _, thr = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    out_file = captcha_file + "_clean.png"
    cv2.imwrite(out_file, thr)

    p = subprocess.Popen(
        ["tesseract", out_file, "stdout",
         "--oem","1","--psm","8",
         "-c","tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789"],
        stdout=subprocess.PIPE
    )

    captcha = p.communicate()[0].decode().strip()

    return captcha


def search_advocate(name):

    session = requests.Session()
    headers = {"user-agent":"Mozilla/5.0"}

    r = session.get(
        BASE + "cases/qs_civil_advocate.php?state_cd=1&dist_cd=1&court_code=1&stateNm=",
        headers=headers
    )

    soup = BeautifulSoup(r.text,"html.parser")
    csrf = soup.find("input",{"name":"__csrf_magic"})["value"]

    captcha = solve_captcha(session, headers)

    print("Captcha solved:", captcha)

    today = datetime.date.today().strftime("%d-%m-%Y")

    payload = {
        "__csrf_magic": csrf,
        "radAdvt":"1",
        "advocate_name": name,
        "caselist_date": today,
        "f":"Pending",
        "captcha": captcha,
        "submit1":"Go"
    }

    r2 = session.post(
        BASE + "cases/qs_civil_advocate.php?state_cd=1&dist_cd=1&court_code=1&stateNm=",
        data=payload,
        headers={
            **headers,
            "Referer": BASE + "cases/qs_civil_advocate.php"
        }
    )

    return r2.text

