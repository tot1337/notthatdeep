import requests
import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

POST_URL = "https://api.rolimons.com/tradeads/v1/createad"
ROLIMONS_HOME = "https://www.rolimons.com/"
MAX_RETRIES = 3
RETRY_DELAY = 10  # seconds

# your payload
JSON_BODY = {
    "player_id": 2251466007,
    "offer_item_ids": [1609401184],
    "request_item_ids": [],
    "request_tags": ["any"]
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": ROLIMONS_HOME,
    "Content-Type": "application/json",
    "Origin": ROLIMONS_HOME
}

def get_fresh_token(session: requests.Session):
    """Fetch the main page to get a fresh _RoliVerification cookie."""
    resp = session.get(ROLIMONS_HOME, headers=HEADERS, timeout=20)
    if "_RoliVerification" not in session.cookies:
        logging.error("Failed to obtain fresh _RoliVerification token")
        return None
    return session.cookies["_RoliVerification"]

def send_post(session: requests.Session):
    """Send POST with fresh token."""
    for attempt in range(1, MAX_RETRIES + 1):
        token = get_fresh_token(session)
        if not token:
            logging.warning("No token, retrying in %ds...", RETRY_DELAY)
            time.sleep(RETRY_DELAY)
            continue

        # attach cookies
        session.cookies["_RoliVerification"] = token
        # _RoliData can stay from initial session if present
        logging.info("Using fresh token: %s...", token[:10])

        try:
            resp = session.post(POST_URL, headers=HEADERS, json=JSON_BODY, timeout=20)
            logging.info("POST attempt %d: status %s", attempt, resp.status_code)
            logging.info("Response: %s", resp.text[:200])  # log first 200 chars
            if resp.status_code == 200:
                logging.info("POST successful")
                return True
        except requests.RequestException as e:
            logging.warning("Request failed: %s", e)

        logging.info("Retrying in %ds...", RETRY_DELAY)
        time.sleep(RETRY_DELAY)
    logging.error("All retries failed")
    return False

def main():
    session = requests.Session()
    send_post(session)

if __name__ == "__main__":
    main()
