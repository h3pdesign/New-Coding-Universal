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


# Function to clean tags
def clean_tags(tags):
    cleaned = []
    for tag in tags:
        cleaned_tag = re.sub(r"[\*\n\-\d\.\s]+", "", tag).strip()
        if cleaned_tag:
            cleaned.append(cleaned_tag)
    return cleaned


# Function to get tags from Grok API
def get_tags_from_grok(content_or_title):
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "grok-beta",
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
    except requests.exceptions.RequestException as e:
        print(f"Error with Grok API: {str(e)}")
        return []


# Function to fetch all Pocket articles
def fetch_pocket_articles():
    all_articles = {}
    offset = 0
    count = 100  # Adjust if needed, max 9999

    while True:
        try:
            print(f"Fetching articles: count={count}, offset={offset}")
            response = pocket.get(detail_type="complete", count=count, offset=offset)
            articles = response[0].get("list", {})
            all_articles.update(articles)

            if len(articles) < count:
                break

            offset += count
            print(f"Fetched {len(all_articles)} articles so far...")
            time.sleep(1)  # Mitigate rate limiting

        except Exception as e:
            print(f"Error fetching Pocket articles: {str(e)}")
            if hasattr(e, "response") and e.response:
                print(f"Response details: {e.response.text}")
            if "403" in str(e):
                print("Permission error: Check your access token permissions.")
            elif "429" in str(e):
                print("Rate limit exceeded: Wait and try again later.")
            elif "400" in str(e):
                print("Bad request: Check parameters or offset.")
            return None

    return all_articles


# Function to tag articles in Pocket
def tag_pocket_articles(article_tags_dict):
    actions = [
        {"action": "tags_add", "item_id": item_id, "tags": ",".join(clean_tags(tags))}
        for item_id, tags in article_tags_dict.items()
        if tags
    ]
    if actions:
        try:
            pocket.bulk_add(actions)
            pocket.commit()
            print(f"Tagged {len(actions)} articles in bulk")
        except Exception as e:
            print(f"Error bulk tagging: {str(e)}")


# Main execution
def main():
    articles = fetch_pocket_articles()
    if articles is not None:
        print(f"Found {len(articles)} articles in your Pocket account.")
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
        tag_pocket_articles(article_tags)
    else:
        print("Failed to fetch articles. Check the error message above for details.")


if __name__ == "__main__":
    main()
