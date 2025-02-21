import os
import time
import requests
import re
import json
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
    retries = 5
    for attempt in range(retries):
        try:
            response = pocket.get(count=1)
            if "error" in response[0]:
                raise ValueError(f"Pocket API error: {response[0]['error']}")
            articles = response[0].get("list", {})
            print(f"Test fetch successful: Retrieved {len(articles)} article(s)")
            return True
        except Exception as e:
            print(f"Test fetch failed on attempt {attempt + 1}/{retries}: {str(e)}")
            if hasattr(e, "response") and e.response:
                print(f"Response status: {e.response.status_code}")
                print(f"Response details: {e.response.text}")
            if attempt < retries - 1:
                delay = 30
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print("All retries failed. Pocket API may be down or token invalid.")
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


# Function to fetch a batch of 1000 untagged Pocket articles in smaller sub-batches
def fetch_pocket_articles(offset=0, total_batch_size=1000, sub_batch_size=100):
    all_articles = {}
    articles_fetched = 0
    sub_offset = offset

    while articles_fetched < total_batch_size:
        remaining = total_batch_size - articles_fetched
        current_batch = min(sub_batch_size, remaining)
        retries = 3
        for attempt in range(retries):
            try:
                print(
                    f"Fetching {current_batch} untagged articles at offset {sub_offset}, attempt {attempt + 1}/{retries}"
                )
                response = pocket.get(
                    count=current_batch, offset=sub_offset, tag="_untagged_"
                )
                if "error" in response[0]:
                    raise ValueError(f"Pocket API error: {response[0]['error']}")
                articles = response[0].get("list", {})
                all_articles.update(articles)
                articles_fetched += len(articles)
                print(f"Fetched {articles_fetched} untagged articles so far")
                sub_offset += current_batch
                if (
                    len(articles) < current_batch
                ):  # Fewer than requested, likely end of untagged
                    print(f"Reached end of untagged articles at {articles_fetched}")
                    return all_articles
                break
            except Exception as e:
                print(f"Error fetching Pocket articles: {str(e)}")
                if hasattr(e, "response") and e.response:
                    print(f"Response status: {e.response.status_code}")
                    print(f"Response details: {e.response.text}")
                if attempt < retries - 1:
                    delay = 5
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print("All retries failed for this sub-batch.")
                    return None
        if articles_fetched >= total_batch_size:
            break

    return all_articles


# Function to tag articles in Pocket using raw API
def tag_pocket_articles(article_tags_dict):
    actions = [
        {
            "action": "tags_add",
            "item_id": str(item_id),
            "tags": ",".join(clean_tags(tags)),
        }
        for item_id, tags in article_tags_dict.items()
        if tags
    ]
    if actions:
        print(f"Preparing to tag {len(actions)} articles.")
        print("Sample action:", actions[0])
        url = "https://getpocket.com/v3/send"
        headers = {"Content-Type": "application/json"}
        payload = {
            "consumer_key": POCKET_CONSUMER_KEY,
            "access_token": POCKET_ACCESS_TOKEN,
            "actions": actions,
        }
        retries = 3
        for attempt in range(retries):
            try:
                response = requests.post(
                    url, data=json.dumps(payload), headers=headers, timeout=30
                )
                response.raise_for_status()
                print(f"Tagged {len(actions)} articles in bulk")
                print(f"Response: {response.json()}")

                # Verify the first article
                sample_id = actions[0]["item_id"]
                sample_tags = actions[0]["tags"].split(",")
                verify_response = pocket.get(item_id=sample_id)
                tagged_article = verify_response[0]["list"].get(sample_id, {})
                applied_tags = list(tagged_article.get("tags", {}).keys())
                print(
                    f"Verification - Article {sample_id} (Title: {tagged_article.get('resolved_title', 'Untitled')})"
                )
                print(f"Expected tags: {sample_tags}")
                print(f"Applied tags: {applied_tags}")
                if set(sample_tags) == set(applied_tags):
                    print("Success: Tags verified as applied correctly")
                else:
                    print("Warning: Tags not applied as expected")
                break
            except requests.exceptions.ReadTimeout as e:
                print(f"Timeout error on attempt {attempt + 1}/{retries}: {e}")
                if attempt < retries - 1:
                    print("Retrying in 10 seconds...")
                    time.sleep(10)
                else:
                    print("Max retries reached")
                    raise
            except requests.exceptions.HTTPError as e:
                print(f"Error bulk tagging: {e}")
                print(f"Response status: {e.response.status_code}")
                print(f"Response details: {e.response.text}")
                raise
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                raise


# Main execution for 1000 articles
def main():
    if not test_pocket_connection():
        print(
            "Cannot proceed due to connection failure. Check credentials or Pocket API status."
        )
        return

    # Set offset for this run (adjust manually for each run)
    OFFSET = 0  # Start at 0, then 1000, 2000, etc.
    articles = fetch_pocket_articles(
        offset=OFFSET, total_batch_size=1000, sub_batch_size=100
    )
    if articles is not None:
        print(
            f"Found {len(articles)} untagged articles in your Pocket account for offset {OFFSET}."
        )
        article_tags = {}
        for item_id, article in articles.items():
            title = article.get(
                "resolved_title", article.get("given_title", "Untitled")
            )
            print(f"Processing: {title}")
            tags = get_tags_from_grok(title)
            if tags:
                print(f"Generated tags for '{title}': {tags}")
                article_tags[item_id] = tags
            else:
                print(f"No tags generated for '{title}'")
        if article_tags:
            tag_pocket_articles(article_tags)
        print(
            f"Completed tagging batch at offset {OFFSET}. Next offset: {OFFSET + 1000}"
        )
    else:
        print("Failed to fetch articles. Check the error message above for details.")


if __name__ == "__main__":
    main()
