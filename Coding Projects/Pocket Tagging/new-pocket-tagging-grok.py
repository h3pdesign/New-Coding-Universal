import os
import time
import requests
import re
import json
import logging
import argparse
import pocket
from dotenv import load_dotenv
from collections import defaultdict
from hashlib import md5

# Configure logging
logging.basicConfig(
    filename="pocket_tagging.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Load environment variables from .env file
load_dotenv()
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_URL = "https://api.x.ai/v1/chat/completions"

if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN, GROK_API_KEY]):
    logging.error("Missing required environment variables. Check your .env file.")
    raise ValueError("Missing required environment variables. Check your .env file.")

pocket_instance = pocket.Pocket(
    consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN
)

# Organized common tags by category
COMMON_TAGS = {
    "tech": ["technology", "software", "hardware", "ai", "data", "innovation"],
    "science": ["science", "research", "space", "energy", "environment"],
    "culture": ["art", "music", "film", "literature", "fashion", "culture"],
    "society": ["politics", "economics", "law", "crime", "education"],
    "lifestyle": ["health", "travel", "food", "sports", "productivity"],
}
FLAT_COMMON_TAGS = set(tag for category in COMMON_TAGS.values() for tag in category)

TAG_CACHE_FILE = "pocket_tags_cache.json"
GROK_TAG_CACHE_FILE = "grok_tag_cache.json"
PROCESSED_IDS_FILE = "processed_ids.json"


def load_existing_tags_from_cache():
    if os.path.exists(TAG_CACHE_FILE):
        with open(TAG_CACHE_FILE, "r") as f:
            tags = set(json.load(f))
        logging.info(f"Loaded {len(tags)} existing tags from cache.")
        return tags
    logging.info("No tag cache found. Fetching existing tags from Pocket...")
    all_articles = {}
    offset = 0
    count = 100
    retries = 5
    existing_tags = set()

    while True:
        for attempt in range(retries):
            try:
                response = pocket_instance.get(
                    count=count, offset=offset, detailType="complete", state="all"
                )
                logging.info(f"Pocket API response for tags: {response}")
                articles = response[0].get("list", {})
                all_articles.update(articles)
                for article in articles.values():
                    existing_tags.update(article.get("tags", {}).keys())
                if len(articles) < count:
                    break
                offset += count
                logging.info(f"Fetched {len(all_articles)} articles (Offset: {offset})")
                time.sleep(2)
                break
            except pocket.RateLimitException as e:
                delay = 60 * (attempt + 1)
                logging.warning(f"Rate limit hit: {str(e)}. Retrying in {delay}s...")
                time.sleep(delay)
            except Exception as e:
                delay = 5 * (attempt + 1)
                logging.error(f"Pocket API error: {str(e)}. Retrying in {delay}s...")
                time.sleep(delay)
                if "401" in str(e) or "403" in str(e):
                    logging.error(
                        "Authentication error. Check POCKET_CONSUMER_KEY and POCKET_ACCESS_TOKEN."
                    )
                    raise
        if len(articles) < count:
            break

    with open(TAG_CACHE_FILE, "w") as f:
        json.dump(list(existing_tags), f)
    logging.info(f"Cached {len(existing_tags)} existing tags.")
    return existing_tags


def load_grok_tag_cache():
    if os.path.exists(GROK_TAG_CACHE_FILE):
        with open(GROK_TAG_CACHE_FILE, "r") as f:
            cache = json.load(f)
            logging.info(f"Loaded Grok tag cache with {len(cache)} entries.")
            return cache
    return {}


def save_grok_tag_cache(cache):
    with open(GROK_TAG_CACHE_FILE, "w") as f:
        json.dump(cache, f)
    logging.info("Saved Grok tag cache.")


def load_processed_ids():
    if os.path.exists(PROCESSED_IDS_FILE):
        with open(PROCESSED_IDS_FILE, "r") as f:
            ids = set(json.load(f))
            logging.info(f"Loaded {len(ids)} processed IDs.")
            return ids
    return set()


def save_processed_ids(processed_ids):
    with open(PROCESSED_IDS_FILE, "w") as f:
        json.dump(list(processed_ids), f)
    logging.info(f"Saved {len(processed_ids)} processed IDs.")


def fetch_pocket_articles(
    max_articles=100, processed_ids=None, offset_start=0, force_all=False
):
    if processed_ids is None:
        processed_ids = set()
    logging.info(
        f"Fetching up to {max_articles} articles from offset {offset_start} (force_all={force_all})..."
    )
    all_articles = {}
    offset = offset_start
    count = 50  # Reduced batch size
    retries = 5

    fetch_params = {
        "count": count,
        "offset": offset,
        "detailType": "complete",
        "state": "all",
    }
    if not force_all:
        fetch_params["tag"] = "_untagged_"
        fetch_type = "untagged"
    else:
        fetch_type = "all"

    while len(all_articles) < max_articles:
        for attempt in range(retries):
            try:
                remaining = max_articles - len(all_articles)
                fetch_count = min(count, remaining)
                fetch_params["count"] = fetch_count
                fetch_params["offset"] = offset
                logging.info(
                    f"Fetching {fetch_count} {fetch_type} articles at offset {offset}..."
                )
                response = pocket_instance.get(**fetch_params)
                logging.info(f"Pocket API response ({fetch_type}): {response}")
                articles = response[0].get("list", {})
                filtered_articles = {
                    k: v for k, v in articles.items() if k not in processed_ids
                }
                all_articles.update(filtered_articles)
                if len(articles) < fetch_count:
                    logging.info(
                        f"Finished fetching {fetch_type}. Total: {len(all_articles)}"
                    )
                    break
                offset += fetch_count
                time.sleep(3)  # Increased delay
                break
            except pocket.RateLimitException as e:
                delay = 120 * (attempt + 1)  # Longer delay for rate limits
                logging.warning(f"Rate limit hit: {str(e)}. Retrying in {delay}s...")
                print(f"Rate limit hit. Waiting {delay} seconds before retrying...")
                time.sleep(delay)
            except Exception as e:
                delay = 5 * (attempt + 1)
                logging.error(f"Pocket API error: {str(e)}. Retrying in {delay}s...")
                time.sleep(delay)
                if "401" in str(e) or "403" in str(e):
                    logging.error(
                        "Authentication or permission error. Check POCKET_CONSUMER_KEY and POCKET_ACCESS_TOKEN."
                    )
                    print(
                        "Authentication or permission error. Regenerate POCKET_ACCESS_TOKEN with full permissions."
                    )
                    raise
        if len(articles) < fetch_count:
            break

    if not all_articles and not force_all:
        logging.info("No untagged articles found. Fetching all articles as fallback...")
        return fetch_pocket_articles(
            max_articles, processed_ids, offset_start, force_all=True
        )

    logging.info(f"Fetched {len(all_articles)} articles total.")
    return all_articles


def clean_tag(tag):
    return re.sub(r"[°€\W]+", "", tag).lower().strip()


def is_single_noun(tag):
    cleaned = clean_tag(tag)
    return len(cleaned.split()) == 1


def map_to_common_tags(grok_tags, common_tags, existing_tags):
    mapped_tags = set()
    for tag in grok_tags:
        cleaned_tag = clean_tag(tag)
        if is_single_noun(cleaned_tag):
            if cleaned_tag in common_tags:
                mapped_tags.add(cleaned_tag)
            elif cleaned_tag in existing_tags:
                mapped_tags.add(cleaned_tag)
            else:
                for category, tags in COMMON_TAGS.items():
                    if cleaned_tag in tags or any(
                        cleaned_tag.startswith(t) for t in tags
                    ):
                        mapped_tags.add(next(t for t in tags if t in common_tags))
                        break
    return list(mapped_tags)[:5]


def get_tags_from_grok(content_or_title, grok_cache):
    cache_key = md5(content_or_title.encode()).hexdigest()
    if cache_key in grok_cache:
        logging.info(f"Using cached tags for: {content_or_title[:50]}")
        return grok_cache[cache_key]

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "grok-3",
        "messages": [
            {
                "role": "system",
                "content": "Return 3-5 single-word noun tags (no adjectives, adverbs, verbs, or multi-word phrases) separated by commas.",
            },
            {
                "role": "user",
                "content": f"Generate 3-5 relevant tags for: {content_or_title}",
            },
        ],
        "max_tokens": 50,
        "temperature": 0.7,
    }
    retries = 3
    for attempt in range(retries):
        try:
            time.sleep(1)
            response = requests.post(
                GROK_API_URL, headers=headers, json=payload, timeout=10
            )
            response.raise_for_status()
            tags_text = (
                response.json()
                .get("choices", [{}])[0]
                .get("message", {})
                .get("content", "")
                .strip()
            )
            tags = [tag.strip() for tag in tags_text.split(",")] if tags_text else []
            logging.info(f"Grok-generated tags for '{content_or_title[:50]}': {tags}")
            grok_cache[cache_key] = tags
            save_grok_tag_cache(grok_cache)
            return tags
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                delay = 10 * (attempt + 1)
                logging.warning(
                    f"Grok API rate limit hit, retrying in {delay}s... (Attempt {attempt + 1}/{retries})"
                )
                time.sleep(delay)
            else:
                logging.error(f"Grok API error: {str(e)}")
                return []
        except requests.exceptions.RequestException as e:
            logging.error(f"Grok request error: {str(e)}")
            return []
    return []


def tag_pocket_articles(
    article_tags_dict, processed_ids, common_tags, existing_tags, target_count=100
):
    tagged_count = 0
    for item_id, tags in article_tags_dict.items():
        if tagged_count >= target_count:
            break
        mapped_tags = map_to_common_tags(tags, common_tags, existing_tags)
        if not mapped_tags:
            logging.warning(f"Skipping item {item_id}: No valid tags generated.")
            continue
        tag_string = ",".join(mapped_tags)
        logging.info(f"Tagging item {item_id} with tags: {tag_string}")
        retries = 3
        for attempt in range(retries):
            try:
                pocket_instance.tags_add(item_id, tag_string)
                processed_ids.add(item_id)
                save_processed_ids(processed_ids)
                tagged_count += 1
                logging.info(f"Tagged item {item_id} successfully.")
                time.sleep(3)  # Increased delay
                break
            except pocket.RateLimitException as e:
                delay = 120 * (attempt + 1)
                logging.warning(f"Rate limit hit: {str(e)}. Retrying in {delay}s...")
                print(f"Rate limit hit. Waiting {delay} seconds before retrying...")
                time.sleep(delay)
            except Exception as e:
                logging.error(f"Error tagging item {item_id}: {str(e)}")
                if "401" in str(e) or "403" in str(e):
                    print(
                        "Authentication or permission error. Regenerate POCKET_ACCESS_TOKEN with full permissions."
                    )
                    raise
                break
    logging.info(f"Tagged {tagged_count} articles.")
    return tagged_count


def main():
    parser = argparse.ArgumentParser(
        description="Tag Pocket articles with Grok-generated tags."
    )
    parser.add_argument(
        "--force-all",
        action="store_true",
        help="Force fetch all articles, not just untagged.",
    )
    args = parser.parse_args()

    logging.info("Script started")
    logging.info(f"Consumer Key: {POCKET_CONSUMER_KEY[:10]}...")
    logging.info(f"Access Token: {POCKET_ACCESS_TOKEN[:10]}...")
    logging.info(f"Force all articles: {args.force_all}")

    # Test Pocket API connectivity
    try:
        test_response = pocket_instance.get(count=1, detailType="complete", state="all")
        logging.info(f"Pocket API test response: {test_response}")
        print("Pocket API connection successful.")
    except pocket.RateLimitException as e:
        logging.error(f"Rate limit exceeded: {str(e)}")
        print(
            "Pocket API rate limit exceeded. Please wait at least 1 hour (e.g., until after 11:00 AM on May 5, 2025) and try again."
        )
        print(
            "Alternatively, reduce API calls by setting max_articles_per_run lower in the script."
        )
        print(
            "To ensure full permissions, regenerate POCKET_ACCESS_TOKEN using get_pocket_access_token.py."
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

    existing_tags = load_existing_tags_from_cache()
    common_tags = FLAT_COMMON_TAGS.union(
        {tag for tag in existing_tags if is_single_noun(tag)}
    )
    grok_cache = load_grok_tag_cache()
    processed_ids = load_processed_ids()

    max_articles_per_run = 100  # Reduced to stay within rate limits
    offset = 0

    articles = fetch_pocket_articles(
        max_articles=max_articles_per_run,
        processed_ids=processed_ids,
        offset_start=offset,
        force_all=args.force_all,
    )
    if not articles:
        logging.warning("No articles fetched.")
        print("No articles found. Try the following:")
        print(
            "1. Add untagged articles to your Pocket account (save a webpage without tags)."
        )
        print(
            "2. Run with --force-all to process all articles: python script.py --force-all"
        )
        print("3. Reset cache files: mv *.json backup/")
        print("4. Verify POCKET_CONSUMER_KEY and POCKET_ACCESS_TOKEN in .env.")
        print("Check pocket_tagging.log for detailed API responses.")
        return

    article_tags = {}
    for item_id, article in articles.items():
        if item_id in processed_ids:
            continue
        title = article.get("resolved_title", article.get("given_title", ""))
        excerpt = article.get("excerpt", "")
        url = article.get("resolved_url", article.get("given_url", ""))
        content = title or excerpt or url
        if not content:
            logging.warning(f"Skipping item {item_id}: No usable content")
            processed_ids.add(item_id)
            save_processed_ids(processed_ids)
            continue
        logging.info(f"Processing: {content[:50]}...")
        grok_tags = get_tags_from_grok(content, grok_cache)
        if grok_tags:
            article_tags[item_id] = grok_tags

    if article_tags:
        tagged_count = tag_pocket_articles(
            article_tags,
            processed_ids,
            common_tags,
            existing_tags,
            target_count=max_articles_per_run,
        )
        logging.info(f"Next offset: {offset + tagged_count}")
        print(f"Tagged {tagged_count} articles. Next offset: {offset + tagged_count}")
    else:
        logging.warning("No tags generated for articles.")
        print("No tags generated. Check Grok API or article content.")

    logging.info("Script finished")
    print("Script finished")


if __name__ == "__main__":
    main()
