import os
import time
import requests
import re
from pocket import Pocket
from dotenv import load_dotenv

# Debugging: Confirm script starts
print("Script is loading...")

# Load environment variables from .env file
load_dotenv()

# Pocket and Grok API credentials
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_URL = "https://api.x.ai/v1/chat/completions"

# Validate environment variables
print("Checking environment variables...")
if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN, GROK_API_KEY]):
    raise ValueError("Missing required environment variables. Check your .env file.")
print("Environment variables loaded successfully.")

# Initialize Pocket client
print("Initializing Pocket client...")
pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)
print("Pocket client initialized.")


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
    print(f"Cleaning tags: {tags}")
    cleaned = []
    for tag in tags:
        cleaned_tag = re.sub(r"[*\n\d.\s]+", "", tag).strip()
        if cleaned_tag:
            cleaned.append(cleaned_tag)
    print(f"Cleaned tags: {cleaned}")
    return cleaned


def get_tags_from_grok(content_or_title):
    """Generate tags using Grok API."""
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
    time.sleep(2)  # Initial delay to avoid rate limits
    for attempt in range(retries):
        try:
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
                delay = 60 * (attempt + 1)
                print(
                    f"Rate limit hit, retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})"
                )
                time.sleep(delay)
                if attempt == retries - 1:
                    print(f"Max retries reached, using fallback tag")
                    return ["to_tag_later"]
            else:
                print(f"Grok API HTTP error: {str(e)}")
                return ["to_tag_later"]
        except requests.exceptions.RequestException as e:
            print(f"Grok API request error: {str(e)}")
            return ["to_tag_later"]


def fetch_pocket_articles(max_articles=500):
    """Fetch up to 500 untagged articles from Pocket."""
    print("Fetching up to 500 untagged Pocket articles...")
    all_articles = {}
    offset = 0
    count = 100  # Fetch in batches of 100
    retries = 3
    target = min(max_articles, 500)  # Ensure we don’t exceed 500

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
                all_articles.update(articles)

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


def tag_pocket_articles(article_tags_dict):
    """Tag articles in Pocket with debug output."""
    print("Entering tag_pocket_articles...")
    if not article_tags_dict:
        print("No articles to tag.")
        return

    actions = [
        {"action": "tags_add", "item_id": item_id, "tags": ",".join(clean_tags(tags))}
        for item_id, tags in article_tags_dict.items()
        if tags
    ]
    if not actions:
        print("No valid actions to process.")
        return

    print(f"Preparing to tag {len(actions)} articles. Sample action: {actions[0]}")
    try:
        chunk_size = 50  # Process in chunks of 50 to avoid rate limits
        for i in range(0, len(actions), chunk_size):
            chunk = actions[i : i + chunk_size]
            print(f"Sending chunk {i // chunk_size + 1} with {len(chunk)} actions")
            response = pocket.send(actions=chunk)  # Fixed to use send
            print(
                f"Tagged {len(chunk)} articles in chunk {i // chunk_size + 1}. Response: {response}"
            )
            time.sleep(1)  # Delay between chunks
    except Exception as e:
        print(f"Error bulk tagging: {str(e)}")
        if hasattr(e, "response") and e.response:
            print(f"Response status: {e.response.status_code}")
            print(f"Response details: {e.response.text}")
        raise


def main():
    """Main execution logic for tagging 500 articles."""
    print("Starting main execution...")
    if not test_pocket_connection():
        print(
            "Cannot proceed due to Pocket connection failure. Check credentials and try again."
        )
        return

    articles = fetch_pocket_articles(max_articles=500)
    if articles is not None:
        print(f"Found {len(articles)} untagged articles (limited to 500).")
        article_tags = {}
        for item_id, article in list(articles.items())[:500]:  # Ensure max 500
            title = article.get(
                "resolved_title", article.get("given_title", "Untitled")
            )
            print(f"Processing: {title}")
            tags = get_tags_from_grok(title)
            if tags:
                article_tags[item_id] = tags
        if article_tags:
            tag_pocket_articles(article_tags)
        else:
            print("No tags generated for any articles.")
    else:
        print("Failed to fetch articles.")

    print("Script finished")


if __name__ == "__main__":
    print("Executing main...")
    main()
