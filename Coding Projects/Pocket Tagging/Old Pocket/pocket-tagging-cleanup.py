import os
import time
import re
from pocket import Pocket
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")

if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN]):
    raise ValueError("Missing POCKET_CONSUMER_KEY or POCKET_ACCESS_TOKEN in .env file.")

pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)


def fetch_articles(max_articles=1000, offset_start=0):
    """Fetch up to max_articles from Pocket starting at offset_start."""
    print(
        f"Fetching up to {max_articles} articles from Pocket starting at offset {offset_start}..."
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
                    count=fetch_count, offset=offset, detailType="complete", state="all"
                )
                articles = response[0].get("list", {})
                print(f"Fetched {len(articles)} articles at offset {offset}")
                all_articles.update(articles)
                if len(articles) < fetch_count:
                    print(
                        f"Finished fetching early. Total articles: {len(all_articles)}"
                    )
                    return all_articles
                offset += fetch_count
                time.sleep(1)
                break
            except pocket.RateLimitException as e:
                delay = 60 * (attempt + 1)
                print(f"Rate limit hit: {str(e)}. Retrying in {delay} seconds...")
                time.sleep(delay)
            except pocket.PocketException as e:
                delay = 5 * (attempt + 1)
                print(f"Pocket API error: {str(e)}. Retrying in {delay} seconds...")
                time.sleep(delay)
            except Exception as e:
                print(f"Unexpected error fetching articles: {str(e)}")
                if attempt == retries - 1:
                    return all_articles
                time.sleep(5)
    print(f"Finished fetching. Total articles: {len(all_articles)}")
    return all_articles


def is_compound_tag(tag):
    cleaned = re.sub(r"[°€\W]+", "", tag)
    if len(cleaned) > 3:
        if re.search(r"[a-z][A-Z]", cleaned):
            return True
        if len(cleaned) > 10 and not re.match(r"^[a-z]+$", cleaned):
            return True
    return False


def clean_compound_tags(articles):
    updated_articles = 0
    compound_tags_removed = set()

    for item_id, article in articles.items():
        tags_dict = article.get("tags", {})
        if not tags_dict:
            continue

        original_tags = set(tags_dict.keys())
        compound_tags = {tag for tag in original_tags if is_compound_tag(tag)}
        if compound_tags:
            compound_tags_removed.update(compound_tags)
            tags_to_keep = original_tags - compound_tags
            new_tags = list(tags_to_keep)
            tag_string = ",".join(new_tags) if new_tags else ""
            print(f"Cleaning Item {item_id} - Original tags: {list(original_tags)}")
            print(f"Cleaned tags: {new_tags}")

            retries = 3
            for attempt in range(retries):
                try:
                    pocket.tags_clear(item_id)
                    if tag_string:
                        pocket.tags_add(item_id, tag_string)
                    print(f"Updated item {item_id}")
                    updated_articles += 1
                    time.sleep(0.5)
                    break
                except pocket.RateLimitException as e:
                    delay = 60 * (attempt + 1)
                    print(f"Rate limit hit: {str(e)}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                except pocket.PocketException as e:
                    print(f"Error updating item {item_id}: {str(e)}")
                    break

    print(
        f"Removed {len(compound_tags_removed)} compound tags: {list(compound_tags_removed)[:10]}..."
    )
    print(f"Finished cleaning. Updated {updated_articles} articles.")
    return updated_articles


def main():
    print("Script started")
    print(f"Using Consumer Key: {POCKET_CONSUMER_KEY}")
    print(f"Using Access Token: {POCKET_ACCESS_TOKEN}")

    max_articles_per_run = 1000  # Process 1000 articles per run
    offset = 0  # Adjust manually (0, 1000, 2000, etc.)

    articles = fetch_articles(max_articles=max_articles_per_run, offset_start=offset)
    if articles:
        cleaned_count = clean_compound_tags(articles)
        print(f"Next offset: {offset + len(articles)}")
    else:
        print("No articles fetched.")

    print("Script finished")


if __name__ == "__main__":
    main()
