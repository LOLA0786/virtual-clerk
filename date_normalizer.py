from datetime import datetime
import re

def normalize_date(date_str):

    if not date_str:
        return None

    date_str = date_str.strip()

    # remove "st", "nd", "rd", "th"
    date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)

    formats = [
        "%d %B %Y",
        "%d %b %Y",
        "%d-%m-%Y",
        "%d/%m/%Y"
    ]

    for f in formats:
        try:
            d = datetime.strptime(date_str, f)
            return d.strftime("%Y-%m-%d")
        except:
            pass

    return date_str
