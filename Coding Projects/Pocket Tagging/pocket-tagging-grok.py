import os
import time
import requests
import re
import json
from pocket import Pocket
from dotenv import load_dotenv

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

# File to track processed articles
PROCESSED_FILE = "tagged_articles.json"


def load_processed_articles():
    """Load previously processed article IDs from file."""
    if os.path.exists(PROCESSED_FILE):
        with open(PROCESSED_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_processed_articles(processed_ids):
    """Save processed article IDs to file."""
    with open(PROCESSED_FILE, "w") as f:
        json.dump(list(processed_ids), f)


def test_pocket_connection():
    """Test connectivity to Pocket API."""
    print("Testing Pocket API connection...")
    try:
        response = pocket.get(count=1)
        articles = response[0].get("list", {})
        print(f"Test fetch successful: Retrieved {len(articles)} article(s)")
        return True
    except Exception as e:
        print(f"Test fetch failed: {str(e)}")
        return False


def clean_tags(tags):
    """Clean tags by removing unwanted characters."""
    cleaned = []
    for tag in tags:
        cleaned_tag = re.sub(r"[*\n\d.\s]+", "", tag).strip()
        if cleaned_tag:
            cleaned.append(cleaned_tag)
    return cleaned


def get_tags_from_grok(content_or_title, processed_ids, item_id):
    """Generate tags using Grok API with rate limit handling."""
    print(f"Requesting tags for: {content_or_title}")
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
    initial_delay = 5  # Increased initial delay to 5 seconds
    for attempt in range(retries):
        try:
            time.sleep(initial_delay)
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
            cleaned_tags = clean_tags(tags)
            print(f"Generated tags: {cleaned_tags}")
            return cleaned_tags
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                delay = 60 * (attempt + 1)  # Exponential backoff: 60s, 120s, etc.
                print(
                    f"Rate limit hit, retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})"
                )
                if attempt == retries - 1:
                    print(
                        f"Max retries reached for item {item_id}. Saving progress and exiting."
                    )
                    return None  # Signal to save and exit
                time.sleep(delay)
            else:
                print(f"Grok API HTTP error: {str(e)}")
                return ["to_tag_later"]
        except requests.exceptions.RequestException as e:
            print(f"Grok API request error: {str(e)}")
            return ["to_tag_later"]


def fetch_pocket_articles(max_articles=500, processed_ids=None):
    """Fetch up to 500 untagged articles from Pocket, skipping processed ones."""
    if processed_ids is None:
        processed_ids = set()
    print("Fetching up to 500 untagged Pocket articles...")
    all_articles = {}
    offset = 0
    count = 100
    retries = 3
    target = min(max_articles, 500)

    while len(all_articles) < target:
        for attempt in range(retries):
            try:
                remaining = target - len(all_articles)
                fetch_count = min(count, remaining)
                print(
                    f"Fetching: count={fetch_count}, offset={offset}, attempt={attempt + 1}"
                )
                response = pocket.get(
                    count=fetch_count, offset=offset, tag="_untagged_"
                )
                articles = response[0].get("list", {})
                # Filter out already processed articles
                filtered_articles = {
                    k: v for k, v in articles.items() if k not in processed_ids
                }
                all_articles.update(filtered_articles)

                if len(articles) < fetch_count or len(all_articles) >= target:
                    print(f"Stopping fetch: Retrieved {len(all_articles)} articles")
                    return all_articles

                offset += fetch_count
                print(f"Fetched {len(all_articles)} articles so far...")
                time.sleep(1)
                break
            except Exception as e:
                print(f"Error fetching articles: {str(e)}")
                if hasattr(e, "response") and e.response:
                    print(f"Response status: {e.response.status_code}")
                    print(f"Response details: {e.response.text}")
                if attempt < retries - 1:
                    time.sleep(5)
                else:
                    print("Max retries reached, fetch failed")
                    return all_articles if all_articles else None


def tag_pocket_articles(article_tags_dict, processed_ids):
    """Tag articles in Pocket individually with rate limit handling."""
    if not article_tags_dict:
        print("No articles to tag.")
        return

    print(f"Preparing to tag {len(article_tags_dict)} articles individually.")
    tagged_count = 0
    for item_id, tags in article_tags_dict.items():
        tag_string = ",".join(clean_tags(tags))
        print(f"Tagging item {item_id} with tags: {tag_string}")
        retries = 3
        for attempt in range(retries):
            try:
                pocket.tags_add(item_id, tag_string)
                print(f"Tagged item {item_id} successfully.")
                tagged_count += 1
                processed_ids.add(item_id)  # Mark as processed
                save_processed_articles(processed_ids)  # Save progress
                time.sleep(0.5)  # Delay to avoid Pocket rate limits
                break
            except pocket.RateLimitException:
                delay = 60 * (attempt + 1)
                print(
                    f"Pocket rate limit hit, retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})"
                )
                time.sleep(delay)
                if attempt == retries - 1:
                    print(f"Failed to tag item {item_id} after {retries} attempts.")
            except Exception as e:
                print(f"Error tagging item {item_id}: {str(e)}")
                if hasattr(e, "response") and e.response:
                    print(f"Response status: {e.response.status_code}")
                    print(f"Response details: {e.response.text}")
                break
    print(
        f"Finished tagging. Successfully tagged {tagged_count} out of {len(article_tags_dict)} articles."
    )


def main():
    """Main execution logic for tagging 500 articles with progress tracking."""
    print("Script started")
    if not test_pocket_connection():
        print(
            "Cannot proceed due to Pocket connection failure. Check credentials and try again."
        )
        return

    # Load previously processed articles
    processed_ids = load_processed_articles()
    print(f"Loaded {len(processed_ids)} previously processed article IDs.")

    articles = fetch_pocket_articles(max_articles=500, processed_ids=processed_ids)
    if articles:
        print(f"Found {len(articles)} untagged articles (limited to 500).")
        article_tags = {}
        for item_id, article in list(articles.items())[:500]:
            title = article.get(
                "resolved_title", article.get("given_title", "Untitled")
            )
            print(f"Processing: {title}")
            tags = get_tags_from_grok(title, processed_ids, item_id)
            if tags is None:  # Rate limit exceeded, save and exit
                save_processed_articles(processed_ids)
                print("Script paused due to Grok API rate limits. Resume later.")
                return
            if tags:
                article_tags[item_id] = tags
        if article_tags:
            tag_pocket_articles(article_tags, processed_ids)
        else:
            print("No tags generated for any articles.")
    else:
        print("Failed to fetch articles or no new articles to tag.")

    print("Script finished")


if __name__ == "__main__":
    main()
