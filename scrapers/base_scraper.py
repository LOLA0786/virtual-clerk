import requests
from bs4 import BeautifulSoup
import random
import time

USER_AGENTS = [
"Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
"Mozilla/5.0 (X11; Linux x86_64)",
"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)"
]

def get_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}

def safe_get(url, params=None, timeout=15, retries=3):

    for attempt in range(retries):

        try:

            delay = random.uniform(3,7)
            print(f"Sleeping {delay:.2f}s before request")
            time.sleep(delay)

            resp = requests.get(
                url,
                headers=get_headers(),
                params=params,
                timeout=timeout
            )

            resp.raise_for_status()
            return resp

        except Exception as e:

            print(f"Retry {attempt+1}/{retries} failed: {e}")
            time.sleep(5 * (attempt + 1))

    return None
