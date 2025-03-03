import os
import time
from pocket import Pocket
from dotenv import load_dotenv
from collections import defaultdict
import re

load_dotenv()
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")

if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN]):
    raise ValueError("Missing POCKET_CONSUMER_KEY or POCKET_ACCESS_TOKEN in .env file.")

pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)


def fetch_all_articles():
    print("Fetching all articles from Pocket...")
    all_articles = {}
    offset = 0
    count = 100
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
                time.sleep(1)
                break
            except pocket.RateLimitException as e:
                delay = 60 * (attempt + 1)
                print(
                    f"Rate limit hit: {str(e)}. Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})"
                )
                time.sleep(delay)
            except pocket.PocketException as e:
                delay = 5 * (attempt + 1)
                print(
                    f"Pocket API error: {str(e)}. Retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})"
                )
                time.sleep(delay)


def normalize_tag(tag):
    return re.sub(r"[°€\W]+", "", tag).lower().strip()


def find_duplicate_tags(articles):
    tag_to_articles = defaultdict(set)
    for item_id, article in articles.items():
        tags = article.get("tags", {}).keys()
        for tag in tags:
            tag_to_articles[tag].add(item_id)

    normalized_to_original = defaultdict(list)
    for tag in tag_to_articles.keys():
        normalized = normalize_tag(tag)
        normalized_to_original[normalized].append(tag)

    duplicates = {
        norm: tags for norm, tags in normalized_to_original.items() if len(tags) > 1
    }
    global_tag_counts = {tag: len(tag_to_articles[tag]) for tag in tag_to_articles}

    return duplicates, tag_to_articles, global_tag_counts


def clean_duplicate_tags(articles, duplicates, tag_to_articles):
    updated_articles = 0

    for normalized, duplicate_tags in duplicates.items():
        preferred_tag = max(duplicate_tags, key=lambda t: len(tag_to_articles[t]))
        other_tags = [t for t in duplicate_tags if t != preferred_tag]

        print(f"Merging variants for '{normalized}': {duplicate_tags}")
        print(f"Keeping '{preferred_tag}', removing {other_tags}")

        affected_article_ids = set()
        for tag in duplicate_tags:
            affected_article_ids.update(tag_to_articles[tag])

        for item_id in affected_article_ids:
            current_tags = set(articles[item_id].get("tags", {}).keys())
            new_tags = (current_tags - set(other_tags)) | {preferred_tag}
            tag_string = ",".join(new_tags)

            retries = 3
            for attempt in range(retries):
                try:
                    pocket.tags_clear(item_id)
                    if tag_string:
                        pocket.tags_add(item_id, tag_string)
                    print(f"Updated item {item_id} with tags: {tag_string}")
                    updated_articles += 1
                    time.sleep(0.5)
                    break
                except pocket.RateLimitException as e:
                    delay = 60 * (attempt + 1)
                    print(f"Rate limit hit: {str(e)}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                except pocket.PocketException as e:
                    print(f"Pocket API error: {str(e)}. Retrying in {delay} seconds...")
                    time.sleep(delay)

    print(f"Finished cleaning variants. Updated {updated_articles} articles.")


def limit_tag_usage(articles, tag_to_articles, max_articles_per_tag=5):
    """Limit each tag to a maximum number of articles."""
    updated_articles = 0

    for tag, article_ids in tag_to_articles.items():
        if len(article_ids) > max_articles_per_tag:
            excess_ids = list(article_ids)[max_articles_per_tag:]
            print(
                f"Limiting '{tag}' from {len(article_ids)} to {max_articles_per_tag} articles. Removing from {len(excess_ids)} articles."
            )

            for item_id in excess_ids:
                current_tags = set(articles[item_id].get("tags", {}).keys())
                new_tags = current_tags - {tag}
                tag_string = ",".join(new_tags) if new_tags else ""

                retries = 3
                for attempt in range(retries):
                    try:
                        pocket.tags_clear(item_id)
                        if tag_string:
                            pocket.tags_add(item_id, tag_string)
                        print(f"Updated item {item_id} with tags: {tag_string}")
                        updated_articles += 1
                        time.sleep(0.5)
                        break
                    except pocket.RateLimitException as e:
                        delay = 60 * (attempt + 1)
                        print(
                            f"Rate limit hit: {str(e)}. Retrying in {delay} seconds..."
                        )
                        time.sleep(delay)
                    except pocket.PocketException as e:
                        print(
                            f"Pocket API error: {str(e)}. Retrying in {delay} seconds..."
                        )
                        time.sleep(delay)

    print(f"Finished limiting tag usage. Updated {updated_articles} articles.")


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
        duplicates, tag_to_articles, global_tag_counts = find_duplicate_tags(articles)

        # Report duplicates
        if duplicates:
            print(f"Found {len(duplicates)} sets of duplicate tag variants.")
            clean_duplicate_tags(articles, duplicates, tag_to_articles)
        else:
            print("No duplicate tag variants found across articles.")

        # Report global tag stats
        print(f"Total unique tags: {len(global_tag_counts)}")
        print(
            f"Sample of global tag counts: {dict(list(global_tag_counts.items())[:5])}"
        )

        # Debug specific tags
        debug_tags = ["°sound", "€millionorder", "abgelehnteasylbewerber"]
        print("Occurrences of specific tags:")
        for tag in debug_tags:
            print(f"{tag}: {global_tag_counts.get(tag, 0)} articles")

        # Report tags with high usage
        high_usage_tags = {
            tag: count for tag, count in global_tag_counts.items() if count > 1
        }
        print(f"Tags used on multiple articles: {len(high_usage_tags)}")
        print(f"Sample of high-usage tags: {dict(list(high_usage_tags.items())[:5])}")

        # Uncomment to limit tag usage (e.g., max 5 articles per tag)
        # limit_tag_usage(articles, tag_to_articles, max_articles_per_tag=5)
    else:
        print("No articles fetched.")

    print("Script finished")


if __name__ == "__main__":
    main()
