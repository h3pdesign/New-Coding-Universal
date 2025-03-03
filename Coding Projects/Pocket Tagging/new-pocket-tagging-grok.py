import os
import time
import requests
import re
from pocket import Pocket
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables from .env file
load_dotenv()

# Pocket and Grok API credentials
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_URL = "https://api.x.ai/v1/chat/completions"

# Validate environment variables
if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN, GROK_API_KEY]):
    raise ValueError("Missing required environment variables. Check your .env file.")

# Initialize Pocket client
pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)

# Predefined common tags (expand this list based on your needs)
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
    "machinelearning",
    "statistics",
    "energy",
    "infrastructure",
    "media",
    "socialmedia",
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


# Load existing tags from Pocket (optional)
def load_existing_tags():
    print("Loading existing tags from Pocket...")
    all_articles = {}
    offset = 0
    count = 100
    existing_tags = set()

    while True:
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
            time.sleep(1)
        except Exception as e:
            print(f"Error loading tags: {str(e)}")
            break

    print(f"Loaded {len(existing_tags)} existing tags.")
    return existing_tags


def clean_tag(tag):
    return re.sub(r"[°€\W]+", "", tag).lower().strip()


def map_to_common_tags(grok_tags, common_tags, existing_tags):
    """Map Grok-generated tags to common/existing tags."""
    mapped_tags = set()
    for tag in grok_tags:
        cleaned_tag = clean_tag(tag)
        # Check if it matches existing tags first
        for existing in existing_tags:
            if cleaned_tag in clean_tag(existing) or clean_tag.startswith(
                clean_tag(existing)
            ):
                mapped_tags.add(existing)
                break
        else:
            # Then check common tags
            for common in common_tags:
                if cleaned_tag in common or clean_tag.startswith(common[:3]):
                    mapped_tags.add(common)
                    break
            else:
                # If no match, use the cleaned tag if in common set, else skip
                if cleaned_tag in common_tags:
                    mapped_tags.add(cleaned_tag)

    # Limit to 3 tags max
    return list(mapped_tags)[:3]


def get_tags_from_grok(content_or_title):
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "grok-2-1212",
        "messages": [
            {
                "role": "system",
                "content": "Return plain text tags separated by commas, no markdown.",
            },
            {
                "role": "user",
                "content": f"Generate 3-5 relevant tags for: {content_or_title}",
            },
        ],
        "max_tokens": 50,
        "temperature": 0.7,
    }
    retries = 5
    for attempt in range(retries):
        try:
            time.sleep(5)  # Increased delay to avoid rate limits
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
            print(f"Grok-generated tags: {tags}")
            return tags
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                delay = 60 * (attempt + 1)
                print(
                    f"Rate limit hit, retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})"
                )
                time.sleep(delay)
            else:
                print(f"Grok API error: {str(e)}")
                return ["misc"]
        except requests.exceptions.RequestException as e:
            print(f"Grok request error: {str(e)}")
            return ["misc"]


def fetch_pocket_articles(max_articles=500, processed_ids=None):
    if processed_ids is None:
        processed_ids = set()
    all_articles = {}
    offset = 0
    count = 100
    target = min(max_articles, 500)

    while len(all_articles) < target:
        try:
            remaining = target - len(all_articles)
            fetch_count = min(count, remaining)
            print(f"Fetching: count={fetch_count}, offset={offset}")
            response = pocket.get(count=fetch_count, offset=offset, tag="_untagged_")
            articles = response[0].get("list", {})
            filtered_articles = {
                k: v for k, v in articles.items() if k not in processed_ids
            }
            all_articles.update(filtered_articles)
            if len(articles) < fetch_count:
                break
            offset += fetch_count
            time.sleep(1)
        except Exception as e:
            print(f"Error fetching articles: {str(e)}")
            break

    print(f"Fetched {len(all_articles)} untagged articles.")
    return all_articles


def tag_pocket_articles(article_tags_dict, processed_ids, common_tags, existing_tags):
    tagged_count = 0
    for item_id, tags in article_tags_dict.items():
        mapped_tags = map_to_common_tags(tags, common_tags, existing_tags)
        if not mapped_tags:
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
            except pocket.RateLimitException as e:
                delay = 60 * (attempt + 1)
                print(
                    f"Pocket rate limit hit: {str(e)}. Retrying in {delay} seconds..."
                )
                time.sleep(delay)
            except Exception as e:
                print(f"Error tagging item {item_id}: {str(e)}")
                break
    print(f"Tagged {tagged_count} articles.")


def main():
    print("Script started")

    processed_ids = set()  # Replace with file-based tracking if needed
    existing_tags = load_existing_tags()  # Load current tags
    common_tags = COMMON_TAGS.union(existing_tags)  # Combine with predefined tags

    articles = fetch_pocket_articles(max_articles=500, processed_ids=processed_ids)
    if articles:
        article_tags = {}
        for item_id, article in articles.items():
            title = article.get(
                "resolved_title", article.get("given_title", "Untitled")
            )
            print(f"Processing: {title}")
            grok_tags = get_tags_from_grok(title)
            if grok_tags:
                article_tags[item_id] = grok_tags
        if article_tags:
            tag_pocket_articles(article_tags, processed_ids, common_tags, existing_tags)

    print("Script finished")


if __name__ == "__main__":
    main()
