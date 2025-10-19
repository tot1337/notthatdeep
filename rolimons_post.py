import requests
import logging
import time
import os
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

POST_URL = "https://api.rolimons.com/tradeads/v1/createad"

# payload
JSON_BODY = {
    "player_id": 2251466007,
    "offer_item_ids": [1609401184],
    "request_item_ids": [],
    "request_tags": ["any"]
}

# headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://www.rolimons.com/",
    "Content-Type": "application/json",
    "Origin": "https://www.rolimons.com"
}

# permanent cookies
COOKIES = {
    "_RoliVerification": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJzaW9uIjoxLCJwbGF5ZXJfZGF0YSI6eyJuYW1lIjoiMGhBbmpwIiwiaWQiOjIyNTE0NjYwMDd9LCJpYXQiOjE3NTcwMTY5MjYsImV4cCI6MTc2NDc5Mjk4Nn0.KhapXK4BIe_3Y4BvNqTfQUZewjM2kbEsUJ8YF9jQKWc",
    "_RoliData": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJzaW9uIjoxLCJwbGF5ZXJfZGF0YSI6eyJuYW1lIjoiMGhBbmpwIiwiaWQiOjIyNTE0NjYwMDd9LCJpYXQiOjE3NTcwMTY5MjYsImV4cCI6MTc2NDc5Mjk4Nn0.A8d7c8BYbky5Vm0q9t2nplMhN6-h6JYrne3iyfwl4-UE"
}

STATE_FILE = "last_run.json"
MAX_RETRIES = 3
RETRY_DELAY = 10  # seconds

def set_last_run():
    with open(STATE_FILE, "w") as f:
        json.dump({"last_run": datetime.utcnow().isoformat()}, f)

def send_post():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.post(POST_URL, headers=HEADERS, cookies=COOKIES, json=JSON_BODY, timeout=20)
            logging.info("Attempt %d: HTTP %s", attempt, resp.status_code)
            logging.info("Response: %s", resp.text[:200])
            if resp.status_code == 200:
                logging.info("POST successful")
                set_last_run()
                return
            else:
                logging.warning("POST failed, retrying in %ds...", RETRY_DELAY)
        except requests.RequestException as e:
            logging.error("Request error: %s, retrying in %ds...", e, RETRY_DELAY)
        time.sleep(RETRY_DELAY)

    logging.error("All retries failed")

if __name__ == "__main__":
    send_post()
