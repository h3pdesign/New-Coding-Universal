import os
import json
import logging
import time
import requests
from dotenv import load_dotenv
from pocket import Pocket
from requests.exceptions import RequestException

load_dotenv()

POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")
TAGGED_EXPORT_FILE = os.getenv("TAGGED_EXPORT_FILE")
LOG_FILE = os.getenv("LOG_FILE")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)

required_vars = {
    "POCKET_CONSUMER_KEY": POCKET_CONSUMER_KEY,
    "POCKET_ACCESS_TOKEN": POCKET_ACCESS_TOKEN,
    "TAGGED_EXPORT_FILE": TAGGED_EXPORT_FILE,
    "LOG_FILE": LOG_FILE,
}
for var_name, var_value in required_vars.items():
    if not var_value:
        logging.error("Environment variable %s is not set.", var_name)
        raise ValueError(f"Missing environment variable: {var_name}")

pocket = Pocket(POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN)


def get_existing_urls():
    logging.info("Fetching existing Pocket URLs...")
    existing_urls = set()
    offset = 0
    count = 200
    retries = 3
    while True:
        for attempt in range(retries):
            try:
                response = pocket.get(count=count, offset=offset, detailType="simple")
                if isinstance(response, tuple):
                    data, _ = response
                else:
                    data = response
                if data.get("status") != 1:
                    logging.error("Failed to fetch Pocket data: %s", data)
                    break
                items = data.get("list", {})
                if not items:
                    return existing_urls
                for item in items.values():
                    existing_urls.add(item.get("resolved_url") or item.get("given_url"))
                offset += count
                logging.info("Fetched %d URLs so far...", len(existing_urls))
                time.sleep(20)  # Slower rate
                break
            except RequestException as e:
                logging.error(
                    "Fetch attempt %d/%d failed: %s", attempt + 1, retries, str(e)
                )
                if attempt + 1 < retries:
                    time.sleep(20 * (attempt + 1))
                else:
                    logging.error("Failed to fetch URLs after %d retries.", retries)
                    return existing_urls


def test_api_connection():
    logging.info("Testing Pocket API connection...")
    try:
        response = pocket.get(count=1)
        if isinstance(response, tuple):
            data, _ = response
        else:
            data = response
        if data.get("status") == 1:
            logging.info(
                "API connection successful. Retrieved %d items.",
                len(data.get("list", {})),
            )
        else:
            logging.error("API test failed: %s", data)
    except Exception as e:
        logging.error("API connection failed: %s", str(e))


def import_tagged_articles():
    logging.info("Starting import of tagged articles into Pocket...")
    if not os.path.exists(TAGGED_EXPORT_FILE):
        logging.error("%s not found.", TAGGED_EXPORT_FILE)
        return

    try:
        with open(TAGGED_EXPORT_FILE, "r", encoding="utf-8") as f:
            articles = json.load(f)
        logging.info("Loaded %d articles from %s.", len(articles), TAGGED_EXPORT_FILE)
    except Exception as e:
        logging.error("Failed to load %s: %s", TAGGED_EXPORT_FILE, str(e))
        return

    existing_urls = get_existing_urls()
    actions = [
        {"action": "add", "url": a["url"], "title": a["title"], "tags": a["tags"]}
        for a in articles
        if "url" in a and "title" in a and "tags" in a and a["url"] not in existing_urls
    ]
    logging.info(
        "Prepared %d new actions after deduplication (out of %d total).",
        len(actions),
        len(articles),
    )

    url = "https://getpocket.com/v3/send"
    headers = {"Content-Type": "application/json"}
    batch_size = 50
    total_batches = (len(actions) + batch_size - 1) // batch_size

    last_success = 0
    try:
        with open(LOG_FILE, "r") as log:
            for line in reversed(log.readlines()):
                if "Batch" in line and "successfully imported" in line:
                    last_success = int(line.split("Batch")[1].split()[0])
                    break
        logging.info("Resuming from batch %d", last_success)
    except:
        logging.info("No prior log, starting from scratch.")

    start_index = last_success * batch_size
    max_retries = 3
    rate_limit_wait = False
    for i in range(start_index, len(actions), batch_size):
        if rate_limit_wait:
            logging.info("Rate limit hit, waiting 1 hour before resuming...")
            time.sleep(3600)  # Wait 1 hour
            rate_limit_wait = False

        batch_num = i // batch_size + 1
        batch = actions[i : i + batch_size]
        logging.info(
            "Processing batch %d of %d with %d articles...",
            batch_num,
            total_batches,
            len(batch),
        )

        payload = {
            "consumer_key": POCKET_CONSUMER_KEY,
            "access_token": POCKET_ACCESS_TOKEN,
            "actions": batch,
        }
        success = False
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    url, headers=headers, data=json.dumps(payload), timeout=60
                )
                logging.debug(
                    "Batch %d response: HTTP %d, %s",
                    batch_num,
                    response.status_code,
                    response.text,
                )

                if response.status_code in (502, 503, 504):
                    logging.warning(
                        "Batch %d failed with HTTP %d (attempt %d/%d), retrying...",
                        batch_num,
                        response.status_code,
                        attempt + 1,
                        max_retries,
                    )
                    time.sleep(20 * (attempt + 1))
                    continue
                elif response.status_code == 403:
                    logging.error(
                        "Batch %d failed: HTTP 403, rate limit or token issue: %s",
                        batch_num,
                        response.text,
                    )
                    time.sleep(60)
                    continue

                try:
                    data = response.json()
                    if response.status_code == 200 and data.get("status") == 1:
                        results = data.get("action_results", [])
                        successes = sum(1 for r in results if r)
                        if successes == len(batch):
                            logging.info(
                                "Batch %d successfully imported %d articles.",
                                batch_num,
                                successes,
                            )
                            success = True
                        else:
                            logging.warning(
                                "Batch %d partially succeeded: %d/%d imported.",
                                batch_num,
                                successes,
                                len(batch),
                            )
                            if successes == 0:  # All failed, likely rate limit
                                rate_limit_wait = True
                            success = True
                        break
                    else:
                        logging.error(
                            "Batch %d failed: HTTP %d, %s",
                            batch_num,
                            response.status_code,
                            response.text,
                        )
                        break
                except json.JSONDecodeError:
                    logging.error(
                        "Batch %d failed: Non-JSON response: HTTP %d, %s",
                        batch_num,
                        response.status_code,
                        response.text,
                    )
                    time.sleep(20 * (attempt + 1))
                    continue
            except RequestException as e:
                logging.error(
                    "Batch %d error (attempt %d/%d): %s",
                    batch_num,
                    attempt + 1,
                    max_retries,
                    str(e),
                )
                if attempt + 1 < max_retries:
                    time.sleep(20 * (attempt + 1))
                else:
                    logging.error(
                        "Batch %d failed after %d retries.", batch_num, max_retries
                    )
                    return
        if success:
            time.sleep(20)  # Slower rate: ~3 batches/minute

    logging.info(
        "Import completed up to batch %d.",
        batch_num if "batch_num" in locals() else last_success,
    )


def main():
    test_api_connection()
    if os.path.exists(TAGGED_EXPORT_FILE):
        logging.info("Found existing tagged data, proceeding to import.")
        import_tagged_articles()
    else:
        logging.error("No tagged data found. Run tagging process first.")


if __name__ == "__main__":
    main()
