import os
import time
import requests
import re
import json
import unicodedata
from pocket import Pocket
from dotenv import load_dotenv
from collections import defaultdict
from datetime import datetime

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
    "technologie",
    "science",
    "wissenschaft",
    "history",
    "geschichte",
    "politics",
    "politik",
    "health",
    "gesundheit",
    "environment",
    "umwelt",
    "business",
    "wirtschaft",
    "education",
    "bildung",
    "art",
    "kunst",
    "culture",
    "kultur",
    "sports",
    "sport",
    "travel",
    "reisen",
    "food",
    "essen",
    "music",
    "musik",
    "film",
    "literature",
    "literatur",
    "economics",
    "ökonomie",
    "security",
    "sicherheit",
    "privacy",
    "datenschutz",
    "innovation",
    "research",
    "forschung",
    "data",
    "daten",
    "software",
    "hardware",
    "ai",
    "ki",
    "statistics",
    "statistik",
    "energy",
    "energie",
    "infrastructure",
    "infrastruktur",
    "media",
    "medien",
    "crime",
    "kriminalität",
    "law",
    "recht",
    "war",
    "krieg",
    "space",
    "raumfahrt",
    "archaeology",
    "archäologie",
    "photography",
    "fotografie",
    "gaming",
    "spiele",
    "fashion",
    "mode",
    "design",
    "productivity",
    "produktivität",
}

TAG_CACHE_FILE = "pocket_tags_cache.json"
GROK_TAG_CACHE_FILE = "grok_tag_cache.json"
PROCESSED_IDS_FILE = "processed_ids.json"
TAG_MAPPING_FILE = "tag_mapping.json"  # From cleaning script


def load_existing_tags_from_cache():
    if os.path.exists(TAG_CACHE_FILE):
        with open(TAG_CACHE_FILE, "r") as f:
            tags = set(json.load(f))
        print(f"Loaded {len(tags)} existing tags from cache.")
        return tags
    print("No tag cache found. Starting with empty tag set.")
    return set()


def save_existing_tags_to_cache(tags):
    with open(TAG_CACHE_FILE, "w") as f:
        json.dump(list(tags), f)
    print(f"Saved {len(tags)} existing tags to cache.")


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
            ids = set(json.load(f))
            print(f"Loaded {len(ids)} processed IDs from {PROCESSED_IDS_FILE}.")
            return ids
    print(f"No processed IDs file found at {PROCESSED_IDS_FILE}. Starting fresh.")
    return set()


def save_processed_ids(processed_ids):
    with open(PROCESSED_IDS_FILE, "w") as f:
        json.dump(list(processed_ids), f)
    print(f"Saved {len(processed_ids)} processed IDs to {PROCESSED_IDS_FILE}.")


def load_tag_mapping():
    if os.path.exists(TAG_MAPPING_FILE):
        with open(TAG_MAPPING_FILE, "r") as f:
            mapping = json.load(f)
            print(
                f"Loaded tag mapping with {len(mapping)} entries from {TAG_MAPPING_FILE}."
            )
            return mapping
    print(
        f"No tag mapping file found at {TAG_MAPPING_FILE}. Starting with empty mapping."
    )
    return {}


def clean_tag(tag):
    # Normalize diacritics to ASCII (e.g., über → uber)
    normalized = "".join(
        c for c in unicodedata.normalize("NFKD", tag) if unicodedata.category(c) != "Mn"
    )
    # Replace unwanted characters with hyphens, preserve existing hyphens
    unwanted = r"[°€?!@#$%^&*()+={}[\]|\\:;\"'<>,./\s]+"  # Explicit unwanted chars
    cleaned = re.sub(unwanted, "-", normalized).lower().strip("-")
    # Replace multiple consecutive hyphens with a single hyphen
    cleaned = re.sub(r"-+", "-", cleaned)
    return cleaned if cleaned and len(cleaned) <= 50 else ""  # Pocket tag length limit


def is_single_noun(tag):
    cleaned = clean_tag(tag)
    # Allow compound nouns, reject only specific non-noun suffixes
    return not cleaned.endswith(("ly", "ed", "ing", "al", "ive"))


def fetch_pocket_articles(max_articles=1000, processed_ids=None, offset_start=0):
    if processed_ids is None:
        processed_ids = set()
    print(
        f"Fetching up to {max_articles} untagged articles from Pocket starting at offset {offset_start}..."
    )
    all_articles = {}
    offset = offset_start
    count = min(100, max_articles)
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
                    detailType="complete",
                    state="all",
                    sort="newest",
                )
                articles = response[0].get("list", {})
                print(f"Fetched {len(articles)} articles at offset {offset}")
                untagged_articles = {}
                for k, v in articles.items():
                    tags = v.get("tags", {})
                    has_tags = bool(tags)
                    time_added = int(v.get("time_added", 0))
                    date_added = (
                        datetime.fromtimestamp(time_added).strftime("%Y-%m-%d")
                        if time_added
                        else "Unknown"
                    )
                    title = v.get("resolved_title", v.get("given_title", "Untitled"))
                    if not has_tags and k not in processed_ids:
                        untagged_articles[k] = v
                        print(
                            f"Found untagged article {k}: {title} (Added: {date_added})"
                        )
                    elif has_tags:
                        print(
                            f"Skipped article {k} - has tags: {list(tags.keys())} (Added: {date_added})"
                        )
                    else:
                        print(
                            f"Skipped article {k} - already processed (Added: {date_added})"
                        )
                all_articles.update(untagged_articles)
                if len(articles) < fetch_count:
                    print(
                        f"Finished fetching early. Total untagged: {len(all_articles)} (Total fetched: {len(articles)})"
                    )
                    return all_articles
                offset += fetch_count
                time.sleep(1)
                break
            except Exception as e:
                if "rate limiting" in str(e).lower() or "forbidden" in str(e).lower():
                    delay = 3600 if attempt == 0 else 60 * (attempt + 1)
                    print(f"Rate limit hit: {str(e)}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                    if attempt == retries - 1:
                        print("Max retries reached. Returning partial fetch.")
                        return all_articles
                else:
                    print(f"Unexpected error fetching articles: {str(e)}")
                    if attempt == retries - 1:
                        print("Max retries reached. Returning partial fetch.")
                        return all_articles
                    time.sleep(5)
    print(f"Finished fetching. Total untagged: {len(all_articles)}")
    return all_articles


def map_to_common_tags(grok_tags, common_tags, existing_tags, tag_mapping):
    mapped_tags = set()
    for tag in grok_tags:
        cleaned_tag = clean_tag(tag)
        if cleaned_tag and is_single_noun(cleaned_tag):
            # Apply consolidation mapping if available
            canonical_tag = tag_mapping.get(cleaned_tag, cleaned_tag)
            if canonical_tag in common_tags or canonical_tag in existing_tags:
                mapped_tags.add(canonical_tag)
            else:
                mapped_tags.add(canonical_tag)
                existing_tags.add(canonical_tag)
        else:
            print(f"Rejected tag '{cleaned_tag}' - invalid format")
    return list(mapped_tags) if mapped_tags else []


def get_tags_from_grok(content_or_title, grok_cache):
    cached_tags = grok_cache.get(content_or_title)
    if cached_tags is not None:
        print(f"Using cached tags for '{content_or_title}': {cached_tags}")
        if cached_tags:
            return cached_tags
        else:
            print(f"Skipping empty cached tags for '{content_or_title}' - regenerating")

    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "grok-2-1212",
        "messages": [
            {
                "role": "system",
                "content": "Return plain text noun tags separated by commas. Tags can be single words or compound nouns (e.g., Ballweg-Prozess). No adjectives or multi-phrase tags.",
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
    article_tags_dict,
    processed_ids,
    common_tags,
    existing_tags,
    tag_mapping,
    target_count=1000,
):
    tagged_count = 0
    for item_id, tags in article_tags_dict.items():
        if tagged_count >= target_count:
            break
        mapped_tags = map_to_common_tags(tags, common_tags, existing_tags, tag_mapping)
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
                if "rate limiting" in str(e).lower() or "forbidden" in str(e).lower():
                    delay = 60 * (attempt + 1)
                    print(
                        f"Rate limit hit while tagging: {str(e)}. Retrying in {delay} seconds..."
                    )
                    time.sleep(delay)
                else:
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
    tag_mapping = load_tag_mapping()

    batch_size = 1000
    offset = 0
    total_tagged = 0

    while True:
        print(f"\n=== Tagging Untagged Articles (Batch starting at {offset}) ===")
        articles = fetch_pocket_articles(
            max_articles=batch_size, processed_ids=processed_ids, offset_start=offset
        )
        if not articles:
            print("No more untagged articles to tag in this batch.")
            break
        article_tags = {}
        for item_id, article in articles.items():
            if item_id not in processed_ids:
                title = article.get(
                    "resolved_title", article.get("given_title", "Untitled")
                )
                if title.lower() == "untitled":
                    print(f"Skipping item {item_id}: Title is 'Untitled'")
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
                tag_mapping,
                target_count=batch_size,
            )
            total_tagged += tagged_count
            offset += len(articles)
            save_processed_ids(processed_ids)
            save_existing_tags_to_cache(existing_tags)
            print(f"Total articles tagged so far: {total_tagged}")
        else:
            print("No articles tagged in this batch.")
            offset += len(articles)
            save_processed_ids(processed_ids)
            save_existing_tags_to_cache(existing_tags)

        if len(articles) < batch_size:
            print(
                f"Fewer articles fetched than batch size ({len(articles)} < {batch_size}). Checking next batch..."
            )
            if not fetch_pocket_articles(
                max_articles=1, processed_ids=processed_ids, offset_start=offset
            ):
                print("Confirmed: No more untagged articles remain.")
                break

    print(f"Tagging automation finished. Total tagged: {total_tagged}")


if __name__ == "__main__":
    automate_tagging()
