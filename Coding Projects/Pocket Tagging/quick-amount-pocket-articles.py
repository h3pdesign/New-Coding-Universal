import os
from pocket import Pocket
from dotenv import load_dotenv

load_dotenv()
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")

if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN]):
    raise ValueError("Missing Pocket credentials in .env file.")

pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)


def get_pocket_counts():
    # Get total articles
    print("Fetching total article count...")
    total_articles = 0
    offset = 0
    count = 100
    while True:
        response = pocket.get(count=count, offset=offset, detailType="simple")
        articles = response[0].get("list", {})
        total_articles += len(articles)
        if len(articles) < count:
            break
        offset += count
        print(f"Fetched {total_articles} articles so far...")

    # Get untagged articles
    print("Fetching untagged article count...")
    untagged_articles = 0
    offset = 0
    while True:
        response = pocket.get(
            count=count, offset=offset, tag="_untagged_", detailType="simple"
        )
        articles = response[0].get("list", {})
        untagged_articles += len(articles)
        if len(articles) < count:
            break
        offset += count
        print(f"Fetched {untagged_articles} untagged articles so far...")

    tagged_articles = total_articles - untagged_articles

    print(f"\nTotal articles: {total_articles}")
    print(f"Tagged articles: {tagged_articles}")
    print(f"Untagged articles: {untagged_articles}")


if __name__ == "__main__":
    get_pocket_counts()
