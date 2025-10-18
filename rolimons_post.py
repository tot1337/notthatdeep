import requests
import logging

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
    "_RoliData": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZXJzaW9uIjoxLCJwbGF5ZXJfZGF0YSI6eyJuYW1lIjoiMGhBbmpwIiwiaWQiOjIyNTE0NjYwMDd9LCJpYXQiOjE3NTcwMTY5MjYsImV4cCI6MTc2NDc5Mjk4Nn0.A8d7c8BYbky5Vm0q9t2nplMhN6-h6JYrne3iyfwl4-U"
}

def send_post():
    try:
        resp = requests.post(POST_URL, headers=HEADERS, cookies=COOKIES, json=JSON_BODY, timeout=20)
        logging.info("HTTP %s", resp.status_code)
        logging.info("Response: %s", resp.text)
        if resp.status_code == 200:
            logging.info("POST successful")
        else:
            logging.warning("POST failed")
    except requests.RequestException as e:
        logging.error("Request error: %s", e)

if __name__ == "__main__":
    send_post()
