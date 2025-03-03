import os
import time
from pocket import Pocket
from dotenv import load_dotenv
from collections import defaultdict

# Load environment variables from .env file
load_dotenv()

# Pocket API credentials
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")

# Validate environment variables
if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN]):
    raise ValueError("Missing POCKET_CONSUMER_KEY or POCKET_ACCESS_TOKEN in .env file.")

# Initialize Pocket client
pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)


def fetch_all_articles():
    """Fetch all articles from Pocket with their tags."""
    print("Fetching all articles from Pocket...")
    all_articles = {}
    offset = 0
    count = 100  # Fetch in batches of 100
    retries = 5

    while True:
        for attempt in range(retries):
            try:
                response = pocket.get(
                    count=count, offset=offset, detailType="complete", state="all"
                )
                articles = response[0].get("list", {})
                all_articles.update(articles)
                print(
                    f"Fetched {len(all_articles)} articles so far... (Offset: {offset}, Batch: {len(articles)})"
                )

                if len(articles) < count:
                    print(f"Finished fetching. Total articles: {len(all_articles)}")
                    return all_articles

                offset += count
                time.sleep(1)  # Avoid rate limits
                break
            except pocket.RateLimitException:
                delay = 60 * (attempt + 1)
                print(
                    f"Rate limit hit, retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})"
                )
                time.sleep(delay)
                if attempt == retries - 1:
                    print("Max retries reached. Returning partial fetch.")
                    return all_articles
            except Exception as e:
                print(f"Error fetching articles: {str(e)}")
                if hasattr(e, "response") and e.response:
                    print(f"Response status: {e.response.status_code}")
                    print(f"Response details: {e.response.text}")
                if attempt < retries - 1:
                    time.sleep(5)
                else:
                    print("Max retries reached. Returning partial fetch.")
                    return all_articles


def find_duplicate_tags(articles):
    """Find duplicate tags both per-article and globally."""
    per_article_duplicates = 0
    global_tag_counts = defaultdict(int)
    tag_to_articles = defaultdict(set)

    # Check per-article duplicates and build global tag map
    for item_id, article in articles.items():
        tags_dict = article.get("tags", {})
        if not tags_dict:
            continue

        original_tags = list(tags_dict.keys())
        unique_tags = list(
            dict.fromkeys(original_tags)
        )  # Remove exact duplicates within article
        if len(unique_tags) < len(original_tags):
            per_article_duplicates += 1
            print(
                f"Per-article duplicate in {item_id}: {original_tags} → {unique_tags}"
            )

        # Count global occurrences
        for tag in unique_tags:
            global_tag_counts[tag] += 1
            tag_to_articles[tag].add(item_id)

    # Find global duplicates (tags appearing >1 time across articles)
    global_duplicates = {
        tag: count for tag, count in global_tag_counts.items() if count > 1
    }

    return per_article_duplicates, global_duplicates, tag_to_articles


def clean_duplicate_tags(
    articles, per_article_duplicates, global_duplicates, tag_to_articles
):
    """Clean per-article duplicates only (global cleanup optional)."""
    updated_articles = 0

    if per_article_duplicates > 0:
        for item_id, article in articles.items():
            tags_dict = article.get("tags", {})
            if not tags_dict:
                continue

            original_tags = list(tags_dict.keys())
            unique_tags = list(dict.fromkeys(original_tags))  # Remove exact duplicates
            if len(unique_tags) < len(original_tags):
                tag_string = ",".join(unique_tags)
                retries = 3
                for attempt in range(retries):
                    try:
                        pocket.tags_clear(item_id)
                        if tag_string:
                            pocket.tags_add(item_id, tag_string)
                        print(
                            f"Updated item {item_id}: {original_tags} → {unique_tags}"
                        )
                        updated_articles += 1
                        time.sleep(0.5)
                        break
                    except pocket.RateLimitException:
                        delay = 60 * (attempt + 1)
                        print(
                            f"Rate limit hit, retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})"
                        )
                        time.sleep(delay)
                    except Exception as e:
                        print(f"Error updating item {item_id}: {str(e)}")
                        break

    print(f"Per-article duplicates found: {per_article_duplicates}")
    print(
        f"Global duplicates (tags used across multiple articles): {len(global_duplicates)}"
    )
    if global_duplicates:
        print(
            f"Sample of global duplicates: {dict(list(global_duplicates.items())[:5])}"
        )
    print(
        f"Finished cleaning. Updated {updated_articles} articles with per-article duplicate tags."
    )


def main():
    print("Script started")

    try:
        pocket.get(count=1)
    except Exception as e:
        print(
            f"Cannot proceed due to Pocket connection failure: {str(e)}. Check credentials and try again."
        )
        return

    articles = fetch_all_articles()
    if articles:
        per_article_duplicates, global_duplicates, tag_to_articles = (
            find_duplicate_tags(articles)
        )
        clean_duplicate_tags(
            articles, per_article_duplicates, global_duplicates, tag_to_articles
        )
    else:
        print("No articles fetched.")

    print("Script finished")


if __name__ == "__main__":
    main()
