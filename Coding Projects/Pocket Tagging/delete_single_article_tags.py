import os
import time
import logging
import sys
import re
from pocket import Pocket
from dotenv import load_dotenv
from collections import defaultdict

# Configure logging with file and stderr handlers
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler("pocket_tag_cleanup.log")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)

# Stderr handler
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(stream_handler)

logging.info("Logging initialized")

# Load environment variables from specific .env file
env_path = "/Users/h3p/Coding/New-Coding-Universal/Coding Projects/Pocket Tagging/.env"
load_dotenv(env_path)
logging.info(f"Loaded .env from: {env_path}")

POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")

if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN]):
    logging.error("Missing required environment variables. Check your .env file.")
    raise ValueError("Missing required environment variables. Check your .env file.")

logging.info(f"Using POCKET_CONSUMER_KEY: {POCKET_CONSUMER_KEY[:10]}...")
logging.info(f"Using POCKET_ACCESS_TOKEN: {POCKET_ACCESS_TOKEN[:10]}...")

pocket_instance = Pocket(
    consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN
)


def is_useless_tag(tag):
    """Determine if a tag is useless (e.g., random alphanumeric like '2qrn8z')."""
    # Tag is useless if it's alphanumeric, 5+ characters, no spaces/special chars, and lacks vowels
    return bool(
        re.match(r"^[0-9a-z]{5,}$", tag, re.IGNORECASE)
        and all(vowel not in tag.lower() for vowel in "aeiou")
    )


def fetch_all_articles():  # sourcery skip: low-code-quality
    """Fetch all articles and their tags from Pocket."""
    logging.info("Fetching all articles from Pocket...")
    all_articles = {}
    offset = 0
    count = 50
    retries = 5
    total_expected_articles = None

    while True:
        for attempt in range(retries):
            try:
                response = pocket_instance.get(
                    count=count, offset=offset, detailType="complete", state="all"
                )
                logging.info(f"Raw API response (offset={offset}): {response}")
                if not isinstance(response, tuple) or len(response) < 1:
                    logging.error(f"Invalid API response format: {response}")
                    raise ValueError(f"Invalid API response format: {response}")
                response_data = response[0]
                articles = response_data.get("list", {})
                if not isinstance(articles, dict):
                    logging.error(f"Unexpected 'list' format: {articles}")
                    raise ValueError(f"Unexpected 'list' format: {articles}")
                all_articles |= articles
                logging.info(
                    f"Fetched {len(articles)} articles at offset {offset}. Total: {len(all_articles)}"
                )
                if total_expected_articles is None and "total" in response_data:
                    total_expected_articles = response_data["total"]
                    logging.info(
                        f"API reports total expected articles: {total_expected_articles}"
                    )
                if len(articles) == 0:
                    logging.info(
                        f"No more articles to fetch. Final total: {len(all_articles)}"
                    )
                    return all_articles
                offset += count
                time.sleep(3)
                break
            except pocket.RateLimitException as e:
                delay = 120 * (attempt + 1)
                logging.warning(f"Rate limit hit: {str(e)}. Retrying in {delay}s...")
                print(f"Rate limit hit. Waiting {delay} seconds before retrying...")
                time.sleep(delay)
            except Exception as e:
                delay = 5 * (attempt + 1)
                logging.error(
                    f"Pocket API error (attempt {attempt + 1}/{retries}, offset={offset}): {str(e)}"
                )
                time.sleep(delay)
                if "401" in str(e) or "403" in str(e):
                    logging.error(
                        "Authentication or permission error. Check POCKET_CONSUMER_KEY and POCKET_ACCESS_TOKEN."
                    )
                    raise
        else:
            logging.error(
                f"Failed to fetch articles after {retries} attempts at offset {offset}."
            )
            raise ValueError(f"Failed to fetch articles after {retries} attempts.")


def count_tags(articles):
    """Count articles per tag and identify useless tags."""
    tag_counts = defaultdict(int)
    tag_to_articles = defaultdict(list)
    useless_tags = set()

    for item_id, article in articles.items():
        tags = article.get("tags", {})
        for tag in tags.keys():
            tag_counts[tag] += 1
            tag_to_articles[tag].append(item_id)
            if is_useless_tag(tag):
                useless_tags.add(tag)

    logging.info(f"Found {len(tag_counts)} unique tags: {list(tag_counts.keys())}")
    logging.info(f"Found {len(useless_tags)} useless tags: {list(useless_tags)}")
    return tag_counts, tag_to_articles, useless_tags


def delete_unwanted_tags(tag_counts, tag_to_articles, useless_tags):
    """Delete tags that are associated with only one article or are useless."""
    single_article_tags = [
        tag
        for tag, count in tag_counts.items()
        if count == 1 and tag not in useless_tags
    ]
    unwanted_tags = single_article_tags + list(useless_tags)
    logging.info(
        f"Found {len(single_article_tags)} single-article tags: {single_article_tags}"
    )
    logging.info(f"Found {len(useless_tags)} useless tags: {list(useless_tags)}")
    logging.info(f"Total {len(unwanted_tags)} unwanted tags to delete: {unwanted_tags}")

    deleted_count = 0
    retries = 5

    for tag in unwanted_tags:
        is_useless = tag in useless_tags
        for item_id in tag_to_articles[tag]:
            tag_type = "useless" if is_useless else "single-article"
            logging.info(f"Removing {tag_type} tag '{tag}' from article {item_id}")
            for attempt in range(retries):
                try:
                    pocket_instance.tags_remove(item_id, tag)
                    logging.info(
                        f"Successfully removed {tag_type} tag '{tag}' from article {item_id}"
                    )
                    deleted_count += 1
                    time.sleep(3)
                    break
                except pocket.RateLimitException as e:
                    delay = 120 * (attempt + 1)
                    logging.warning(
                        f"Rate limit hit: {str(e)}. Retrying in {delay}s..."
                    )
                    print(f"Rate limit hit. Waiting {delay} seconds before retrying...")
                    time.sleep(delay)
                except Exception as e:
                    logging.error(
                        f"Error removing {tag_type} tag '{tag}' from article {item_id}: {str(e)}"
                    )
                    if "401" in str(e) or "403" in str(e):
                        print(
                            "Authentication or permission error. Regenerate POCKET_ACCESS_TOKEN with full permissions."
                        )
                        raise
                    break

    logging.info(f"Deleted {deleted_count} unwanted tags (single-article or useless).")
    return deleted_count


def main():
    logging.info("Script started")
    logging.info(f"Consumer Key: {POCKET_CONSUMER_KEY[:10]}...")
    logging.info(f"Access Token: {POCKET_ACCESS_TOKEN[:10]}...")

    # Test Pocket API connectivity
    try:
        test_response = pocket_instance.get(count=1, detailType="complete", state="all")
        logging.info(f"Pocket API test response: {test_response}")
        print("Pocket API connection successful.")
    except pocket.RateLimitException as e:
        logging.error(f"Rate limit exceeded: {str(e)}")
        print(
            "Pocket API rate limit exceeded. Please wait at least 1 hour (e.g., until after 2:00 PM on May 19, 2025) and try again."
        )
        print(
            "Alternatively, regenerate POCKET_ACCESS_TOKEN with full permissions using get_pocket_access_token.py."
        )
        return
    except Exception as e:
        logging.error(f"Pocket API connectivity test failed: {str(e)}")
        print(f"Error connecting to Pocket API: {str(e)}.")
        if "401" in str(e) or "403" in str(e):
            print(
                "Authentication or permission error. Regenerate POCKET_ACCESS_TOKEN with full permissions using get_pocket_access_token.py."
            )
        else:
            print("Check Pocket API status or try again later.")
        return

    # Fetch all articles
    try:
        articles = fetch_all_articles()
    except Exception as e:
        logging.error(f"Failed to fetch articles: {str(e)}")
        print(f"Error fetching articles: {str(e)}")
        return

    if not articles:
        logging.warning("No articles fetched from Pocket account.")
        print(
            "No articles found. Verify your Pocket account has articles at getpocket.com."
        )
        print("Ensure articles are not archived and try adding new ones if needed.")
        print("Check pocket_tag_cleanup.log for API response details.")
        return

    # Count tags and identify single-article and useless tags
    tag_counts, tag_to_articles, useless_tags = count_tags(articles)
    if not tag_counts:
        logging.warning("No tags found in Pocket account.")
        print(
            "No tags found. Add tagged articles to your Pocket account and try again."
        )
        return

    # Delete unwanted tags
    deleted_count = delete_unwanted_tags(tag_counts, tag_to_articles, useless_tags)
    print(f"Deleted {deleted_count} unwanted tags (single-article or useless).")

    logging.info("Script finished")
    print("Script finished")


if __name__ == "__main__":
    main()
