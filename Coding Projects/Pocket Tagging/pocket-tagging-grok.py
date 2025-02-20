import os
import requests
from pocket import Pocket
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Pocket API credentials
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")

# Grok API credentials
GROK_API_KEY = os.getenv("GROK_API_KEY")
GROK_API_URL = "https://api.x.ai/v1/chat/completions"

# Initialize Pocket client
pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)


# Function to get tags from Grok API
def get_tags_from_grok(content_or_title):
    headers = {
        "Authorization": f"Bearer {GROK_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "grok-beta",  # Use the appropriate Grok model
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that generates concise tags based on text input.",
            },
            {
                "role": "user",
                "content": f"Generate 3-5 relevant tags for the following text: {content_or_title}",
            },
        ],
        "max_tokens": 50,
        "temperature": 0.7,
    }

    response = requests.post(GROK_API_URL, headers=headers, json=payload)
    try:
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        result = response.json()
        tags = result["choices"][0]["message"]["content"].strip().split(", ")
        return tags
    except requests.exceptions.HTTPError as e:
        print(f"Error with Grok API: {response.status_code} - {response.text}")
        return []
    except (KeyError, IndexError) as e:
        print(f"Error parsing Grok API response: {e}")
        print(response.text)
        return []


# Function to fetch all Pocket articles
def fetch_pocket_articles():
    articles = pocket.retrieve(detailType="complete")["list"]
    return articles


# Function to tag articles in Pocket
def tag_pocket_article(item_id, tags):
    action = {
        "action": "tags_add",
        "item_id": item_id,
        "tags": ",".join(tags),
        "time": int(os.time()),
    }
    pocket.bulk_add(action)
    pocket.commit()


# Main execution
def main():
    # Fetch all articles
    articles = fetch_pocket_articles()
    print(f"Found {len(articles)} articles in your Pocket account.")

    for item_id, article in articles.items():
        # Use article title or resolved URL content (if available)
        title = article.get("resolved_title", article.get("given_title", "Untitled"))
        print(f"Processing: {title}")

        # Generate tags using Grok
        tags = get_tags_from_grok(title)
        if tags:
            print(f"Generated tags: {tags}")
            # Tag the article in Pocket
            tag_pocket_article(item_id, tags)
        else:
            print(f"No tags generated for {title}")


if __name__ == "__main__":
    main()
