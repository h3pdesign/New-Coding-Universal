import os
import time
from pocket import Pocket
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Pocket API credentials
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")

# Validate environment variables
if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN]):
    raise ValueError("Missing required environment variables. Check your .env file.")

# Initialize Pocket client
pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN)


# Function to fetch all Pocket articles and count tags
# Adjusted function


def get_pocket_stats():
    all_articles = {}
    total_tags = 0
    offset = 0
    count = 100

    while True:
        try:
            print(f"Fetching articles: count={count}, offset={offset}")
            response = pocket.get(detail_type="complete", count=count, offset=offset)
            articles = response[0].get("list", {})
            all_articles.update(articles)

            for article in articles.values():
                tags = article.get("tags", {})
                total_tags += len(tags)

            if len(articles) < count:
                break

            offset += count
            print(f"Fetched {len(all_articles)} articles so far...")
            time.sleep(1)

        except Exception as e:
            print(f"Error fetching Pocket articles: {str(e)}")
            if "400" in str(e):
                print("Bad request: Check parameter syntax or library version.")
            if "403" in str(e):
                print(
                    "Permission error: Check your access token permissions or consumer key."
                )
            elif "429" in str(e):
                print("Pocket API rate limit exceeded: Wait and try again later.")
            return None, None, None

    return len(all_articles), total_tags, all_articles


# Test basic connectivity
def test_pocket_connection():
    try:
        # Minimal request to test credentials
        response = pocket.get(count=1)
        articles = response[0].get("list", {})
        print(f"Test fetch successful: Retrieved {len(articles)} article(s)")
        return True
    except Exception as e:
        print(f"Test fetch failed: {str(e)}")
        return False


# Main execution
def main():
    # First, test the connection
    if not test_pocket_connection():
        print(
            "Cannot proceed due to connection failure. Check credentials and try again."
        )
        return


# Then fetch full stats
# Updated main
def main():
    if not test_pocket_connection():
        print(
            "Cannot proceed due to connection failure. Check credentials and try again."
        )
        return

    total_articles, total_tags, all_articles = get_pocket_stats()
    if total_articles is not None and total_tags is not None:
        print(f"Total number of articles in your Pocket account: {total_articles}")
        print(f"Total number of tags attached to articles: {total_tags}")

        avg_tags = total_tags / total_articles if total_articles > 0 else 0
        print(f"Average tags per article: {avg_tags:.2f}")

        articles_with_no_tags = sum(
            1 for article in all_articles.values() if not article.get("tags")
        )
        print(f"Number of articles with no tags: {articles_with_no_tags}")
    else:
        print(
            "Failed to fetch Pocket stats. Check the error message above for details."
        )


if __name__ == "__main__":
    main()
