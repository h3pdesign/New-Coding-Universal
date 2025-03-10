import os
import time
import requests
import re
import json
from pocket import Pocket
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_URL = "https://api.x.ai/v1/chat/completions"

if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN, GROK_API_KEY]):
    raise ValueError("Missing required environment variables. Check your .env file.")

pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)

COMMON_TAGS = {
    "technology",
    "science",
    "history",
    "politics",
    "health",
    "environment",
    "business",
    "education",
    "art",
    "culture",
    "sports",
    "travel",
    "food",
    "music",
    "film",
    "literature",
    "economics",
    "security",
    "privacy",
    "innovation",
    "research",
    "data",
    "software",
    "hardware",
    "ai",
    "statistics",
    "energy",
    "infrastructure",
    "media",
    "crime",
    "law",
    "war",
    "space",
    "archaeology",
    "photography",
    "gaming",
    "fashion",
    "design",
    "productivity",
}

TAG_CACHE_FILE = "pocket_tags_cache.json"
GROK_TAG_CACHE_FILE = "grok_tag_cache.json"
PROCESSED_IDS_FILE = "processed_ids.json"


def load_existing_tags_from_cache():
    if os.path.exists(TAG_CACHE_FILE):
        with open(TAG_CACHE_FILE, "r") as f:
            tags = set(json.load(f))
        print(f"Loaded {len(tags)} existing tags from cache.")
        return tags
    print("No tag cache found. Fetching existing tags from Pocket...")
    all_articles = {}
    offset = 0
    count = 100
    retries = 5
    existing_tags = set()

    while True:
        for attempt in range(retries):
            try:
                response = pocket.get(
                    count=count, offset=offset, detailType="complete", state="all"
                )
                articles = response[0].get("list", {})
                all_articles.update(articles)
                for article in articles.values():
                    existing_tags.update(article.get("tags", {}).keys())
                if len(articles) < count:
                    break
                offset += count
                print(
                    f"Fetched {len(all_articles)} articles so far... (Offset: {offset})"
                )
                time.sleep(1)
                break
            except Exception as e:
                print(f"Error fetching tags: {str(e)}")
                if attempt == retries - 1:
                    return existing_tags
                time.sleep(5)
        if len(articles) < count:
            break

    with open(TAG_CACHE_FILE, "w") as f:
        json.dump(list(existing_tags), f)
    print(f"Cached {len(existing_tags)} existing tags.")
    return existing_tags


def load_grok_tag_cache():
    if os.path.exists(GROK_TAG_CACHE_FILE):
        with open(GROK_TAG_CACHE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_grok_tag_cache(cache):
    with open(GROK_TAG_CACHE_FILE, "w") as f:
        json.dump(cache, f)


def load_processed_ids():
    if os.path.exists(PROCESSED_IDS_FILE):
        with open(PROCESSED_IDS_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_processed_ids(processed_ids):
    with open(PROCESSED_IDS_FILE, "w") as f:
        json.dump(list(processed_ids), f)


def fetch_pocket_articles(max_articles=1000, processed_ids=None, offset_start=0):
    if processed_ids is None:
        processed_ids = set()
    print(
        f"Fetching up to {max_articles} untagged articles from Pocket starting at offset {offset_start}..."
    )
    all_articles = {}
    offset = offset_start
    count = 100
    retries = 5

    while len(all_articles) < max_articles:
        for attempt in range(retries):
            try:
                remaining = max_articles - len(all_articles)
                fetch_count = min(count, remaining)
                print(f"Fetching {fetch_count} articles at offset {offset}...")
                response = pocket.get(
                    count=fetch_count,
                    offset=offset,
                    tag="_untagged_",
                    detailType="complete",
                )
                articles = response[0].get("list", {})
                filtered_articles = {
                    k: v for k, v in articles.items() if k not in processed_ids
                }
                all_articles.update(filtered_articles)
                if len(articles) < fetch_count:
                    print(
                        f"Finished fetching early. Total articles: {len(all_articles)}"
                    )
                    return all_articles
                offset += fetch_count
                time.sleep(1)
                break
            except Exception as e:
                print(f"Error fetching articles: {str(e)}")
                if attempt == retries - 1:
                    print("Max retries reached. Returning partial fetch.")
                    return all_articles
                time.sleep(5)
    print(f"Finished fetching. Total articles: {len(all_articles)}")
    return all_articles


def clean_tag(tag):
    return re.sub(r"[°€\W]+", "", tag).lower().strip()


def is_single_noun(tag):
    cleaned = clean_tag(tag)
    return len(cleaned.split()) == 1 and not cleaned.endswith(
        ("ly", "ed", "ing", "al", "ive")
    )


def map_to_common_tags(grok_tags, common_tags, existing_tags):
    mapped_tags = set()
    for tag in grok_tags:
        cleaned_tag = clean_tag(tag)
        if is_single_noun(cleaned_tag):  # Accept any single-word noun
            mapped_tags.add(cleaned_tag)
        # Optionally log rejected tags for debugging
        elif cleaned_tag:
            print(f"Rejected tag '{cleaned_tag}' - not a single-word noun")
    return list(mapped_tags) if mapped_tags else []


def get_tags_from_grok(content_or_title, grok_cache):
    cached_tags = grok_cache.get(content_or_title)
    if cached_tags is not None:
        print(f"Using cached tags for '{content_or_title}': {cached_tags}")
        if cached_tags:  # Only return non-empty cached tags
            return cached_tags
        else:
            print(f"Skipping empty cached tags for '{content_or_title}' - regenerating")

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "grok-2-1212",  # Update to "grok-3" if specified
        "messages": [
            {
                "role": "system",
                "content": "Return plain text single-word noun tags separated by commas, no adjectives or multi-word tags.",
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
            time.sleep(0.5)
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
            print(f"Grok-generated tags for '{content_or_title}': {tags}")
            grok_cache[content_or_title] = tags
            save_grok_tag_cache(grok_cache)
            return tags
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                delay = 10 * (attempt + 1)
                print(
                    f"Rate limit hit, retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})"
                )
                time.sleep(delay)
            else:
                print(f"Grok API error: {str(e)}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Grok request error: {str(e)}")
            return []


def tag_pocket_articles(
    article_tags_dict, processed_ids, common_tags, existing_tags, target_count=1000
):
    tagged_count = 0
    for item_id, tags in article_tags_dict.items():
        if tagged_count >= target_count:
            break
        mapped_tags = map_to_common_tags(tags, common_tags, existing_tags)
        if not mapped_tags:
            print(f"Skipping item {item_id}: No valid tags generated from {tags}")
            continue
        tag_string = ",".join(mapped_tags)
        print(f"Tagging item {item_id} with tags: {tag_string}")
        retries = 3
        for attempt in range(retries):
            try:
                pocket.tags_add(item_id, tag_string)
                print(f"Tagged item {item_id} successfully.")
                tagged_count += 1
                processed_ids.add(item_id)
                time.sleep(0.5)
                break
            except Exception as e:
                print(f"Error tagging item {item_id}: {str(e)}")
                if attempt == retries - 1:
                    break
                time.sleep(5)
    print(f"Tagged {tagged_count} articles.")
    return tagged_count


def automate_tagging():
    print("Tagging automation started")
    existing_tags = load_existing_tags_from_cache()
    common_tags = COMMON_TAGS.union(
        {tag for tag in existing_tags if is_single_noun(tag)}
    )
    grok_cache = load_grok_tag_cache()
    processed_ids = load_processed_ids()

    batch_size = 1000
    offset = 0
    total_tagged = 0

    while True:
        print(f"\n=== Tagging Untagged Articles (Batch starting at {offset}) ===")
        articles = fetch_pocket_articles(
            max_articles=batch_size, processed_ids=processed_ids, offset_start=offset
        )
        if not articles:
            print("No more untagged articles to tag.")
            break
        article_tags = {}
        for item_id, article in articles.items():
            if item_id not in processed_ids:
                title = article.get(
                    "resolved_title", article.get("given_title", "Untitled")
                )
                if title.lower() == "untitled":
                    print(f"Skipping item {item_id}: Title is 'Untitled'")
                    processed_ids.add(item_id)
                    continue
                print(f"Processing: {title}")
                grok_tags = get_tags_from_grok(title, grok_cache)
                if grok_tags:
                    article_tags[item_id] = grok_tags
        if article_tags:
            tagged_count = tag_pocket_articles(
                article_tags,
                processed_ids,
                common_tags,
                existing_tags,
                target_count=batch_size,
            )
            total_tagged += tagged_count
            offset += tagged_count
            save_processed_ids(processed_ids)
            print(f"Total articles tagged so far: {total_tagged}")
        else:
            print("No articles tagged in this batch.")
            break

        if len(articles) < batch_size and not article_tags:
            print(
                "Fewer articles fetched and no tags applied. Assuming all untagged articles processed."
            )
            break

    print(f"Tagging automation finished. Total tagged: {total_tagged}")


if __name__ == "__main__":
    automate_tagging()
