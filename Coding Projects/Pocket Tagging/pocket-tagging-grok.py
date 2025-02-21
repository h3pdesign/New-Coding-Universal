import os
import time
import requests
import re
from pocket import Pocket
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Pocket API credentials
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_URL = "https://api.x.ai/v1/chat/completions"

# Validate environment variables
if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN, GROK_API_KEY]):
    raise ValueError("Missing required environment variables. Check your .env file.")

# Initialize Pocket client
pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)


# Function to test Pocket API connectivity
def test_pocket_connection():
    try:
        response = pocket.get(count=1)
        print(f"Raw test response: {response}")
        articles = response[0].get("list", {})
        print(f"Test fetch successful: Retrieved {len(articles)} article(s)")
        return True
    except Exception as e:
        print(f"Test fetch failed: {str(e)}")
        return False


# Function to clean tags
def clean_tags(tags):
    cleaned = []
    for tag in tags:
        cleaned_tag = re.sub(r"[\*\n\-\d\.\s]+", "", tag).strip()
        if cleaned_tag:
            cleaned.append(cleaned_tag)
    return cleaned


# Function to get tags from Grok API (latest: grok-2-1212)
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
    time.sleep(2)
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
            return clean_tags(tags)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                delay = 60 * (attempt + 1)
                print(
                    f"Rate limit hit for '{content_or_title}', retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})"
                )
                time.sleep(delay)
                if attempt == retries - 1:
                    print(
                        f"Max retries reached for '{content_or_title}', using fallback tag"
                    )
                    return ["to_tag_later"]
            else:
                print(f"Error with Grok API: {str(e)}")
                return ["to_tag_later"]
        except requests.exceptions.RequestException as e:
            print(f"Error with Grok API: {str(e)}")
            return ["to_tag_later"]


# Function to fetch untagged Pocket articles
def fetch_pocket_articles():
    all_articles = {}
    offset = 0
    count = 100
    retries = 3

    while True:
        for attempt in range(retries):
            try:
                print(
                    f"Fetching articles: count={count}, offset={offset}, attempt={attempt+1}"
                )
                response = pocket.get(count=count, offset=offset, tag="_untagged_")
                # print(f"Raw response: {response}")
                articles = response[0].get("list", {})
                all_articles.update(articles)

                if len(articles) < count:
                    print(f"Reached end of untagged articles at {len(all_articles)}")
                    return all_articles

                offset += count
                print(f"Fetched {len(all_articles)} articles so far...")
                time.sleep(1)
                break

            except Exception as e:
                print(f"Error fetching Pocket articles: {str(e)}")
                if hasattr(e, "response") and e.response:
                    status = e.response.status_code
                    print(f"Response status: {status}")
                    print(f"Response details: {e.response.text}")
                    if status == 413:
                        count = max(10, count // 2)
                        time.sleep(5)
                        continue
                if attempt < retries - 1:
                    time.sleep(5)
                else:
                    return None


# Function to tag articles in Pocket with debug output
def tag_pocket_articles(article_tags_dict):
    actions = [
        {"action": "tags_add", "item_id": item_id, "tags": ",".join(clean_tags(tags))}
        for item_id, tags in article_tags_dict.items()
        if tags
    ]
    if actions:
        print(
            f"Preparing to tag {len(actions)} articles. Sample action: {actions[0]}"
        )  # Debug sample
        try:
            chunk_size = 9999
            for i in range(0, len(actions), chunk_size):
                chunk = actions[i : i + chunk_size]
                print(f"Sending chunk {i // chunk_size + 1} with {len(chunk)} actions")
                pocket.bulk_add(chunk)
                pocket.commit()
                print(
                    f"Tagged {len(chunk)} articles in bulk (chunk {i // chunk_size + 1})"
                )
                time.sleep(1)
        except Exception as e:
            print(f"Error bulk tagging: {str(e)}")
            if hasattr(e, "response") and e.response:
                print(f"Response status: {e.response.status_code}")
                print(f"Response details: {e.response.text}")
            raise  # Re-raise to see full stack trace


# Main execution
def main():
    if not test_pocket_connection():
        print(
            "Cannot proceed due to connection failure. Check credentials and try again."
        )
        return

    articles = fetch_pocket_articles()
    if articles is not None:
        print(f"Found {len(articles)} untagged articles in your Pocket account.")
        article_tags = {}
        for item_id, article in articles.items():
            title = article.get(
                "resolved_title", article.get("given_title", "Untitled")
            )
            print(f"Processing: {title}")
            tags = get_tags_from_grok(title)
            if tags:
                print(f"Generated tags: {tags}")
                article_tags[item_id] = tags
            else:
                print(f"No tags generated for {title}")
        if article_tags:
            tag_pocket_articles(article_tags)
    else:
        print("Failed to fetch articles. Check the error message above for details.")


if __name__ == "__main__":
    main()
