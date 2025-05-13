import os
import time
from pocket import Pocket
from dotenv import load_dotenv

load_dotenv()
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")

if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN]):
    raise ValueError("Missing POCKET_CONSUMER_KEY or POCKET_ACCESS_TOKEN in .env file.")

pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)


def get_tagged_article_count():
    print("Fetching all articles from Pocket to count tagged ones...")
    all_articles = {}
    offset = 0
    count = 100
    retries = 3
    tagged_so_far = 0

    while True:
        for attempt in range(retries):
            try:
                response = pocket.get(
                    count=count, offset=offset, detailType="complete", state="all"
                )
                articles = response[0].get("list", {})
                all_articles.update(articles)
                batch_tagged = sum(
                    1 for article in articles.values() if article.get("tags")
                )
                tagged_so_far += batch_tagged
                print(
                    f"Fetched {len(all_articles)} articles so far... (Offset: {offset}, Batch: {len(articles)}, Tagged in batch: {batch_tagged}, Total tagged: {tagged_so_far})"
                )

                if len(articles) < count:
                    print(
                        f"Reached end of articles. Total fetched: {len(all_articles)}"
                    )
                    break

                offset += count
                time.sleep(1)
                break
            except pocket.RateLimitException:
                delay = 60 * (attempt + 1)
                print(
                    f"Rate limit hit, retrying in {delay} seconds... (Attempt {attempt + 1}/{retries})"
                )
                time.sleep(delay)
                if attempt == retries - 1:
                    break
            except Exception as e:
                print(f"Error fetching articles: {str(e)}")
                if hasattr(e, "response") and e.response:
                    print(f"Response status: {e.response.status_code}")
                    print(f"Response details: {e.response.text}")
                if attempt == retries - 1:
                    break
                time.sleep(5)

        if len(articles) < count:
            break

    tagged_count = sum(1 for article in all_articles.values() if article.get("tags"))
    untagged_count = len(all_articles) - tagged_count

    print(f"\nTotal articles fetched: {len(all_articles)}")
    print(f"Number of tagged articles: {tagged_count}")
    print(f"Number of untagged articles: {untagged_count}")

    # Log sample of tagged articles
    tagged_sample = [
        (
            article.get("resolved_title", "Untitled"),
            list(article.get("tags", {}).keys()),
        )
        for article in all_articles.values()
        if article.get("tags")
    ][:5]
    print(f"Sample of tagged articles (title, tags): {tagged_sample}")

    return tagged_count


if __name__ == "__main__":
    get_tagged_article_count()
