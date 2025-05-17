import os
import time
import logging
import sys
from pocket import Pocket
import pocket  # Added for RateLimitException
from dotenv import load_dotenv
from collections import defaultdict
import json
import signal

# Configure logging with file and stderr handlers
logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("pocket_tagging.log")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(file_handler)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)
logger.addHandler(stream_handler)

logging.info("Logging initialized")

# Load environment variables
env_path = "/Users/h3p/Coding/New-Coding-Universal/Coding Projects/Pocket Tagging/.env"
load_dotenv(env_path)
logging.info(f"Loaded .env from: {env_path}")

POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")
GROK_API_KEY = os.getenv("GROK_API_KEY")

if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN, GROK_API_KEY]):
    logging.error("Missing required environment variables. Check your .env file.")
    raise ValueError("Missing required environment variables. Check your .env file.")

logging.info(f"Using POCKET_CONSUMER_KEY: {POCKET_CONSUMER_KEY[:10]}...")
logging.info(f"Using POCKET_ACCESS_TOKEN: {POCKET_ACCESS_TOKEN[:10]}...")

pocket_instance = Pocket(
    consumer_key=POCKET_CONSUMER_KEY, access_token=POCKET_ACCESS_TOKEN
)


# Timeout handler for API calls
def timeout_handler(signum, frame):
    raise TimeoutError("Pocket API call timed out")


# Simulated Grok API response (replace with actual Grok API call)
def generate_tags_with_grok(title, excerpt, url):
    """Simulate Grok API to generate tags based on article content."""
    # Placeholder. In production, call xAI Grok API with GROK_API_KEY.
    content = f"{title} {excerpt}".lower()
    general_tags = []
    specific_tag = ""

    # General tag rules (one-word, broad categories)
    if any(word in content for word in ["news", "politics", "election", "government"]):
        general_tags.extend(["news", "politics"])
    elif any(word in content for word in ["tech", "technology", "ai", "software"]):
        general_tags.extend(["tech", "innovation"])
    elif any(word in content for word in ["science", "research", "study"]):
        general_tags.extend(["science", "research"])
    else:
        general_tags.extend(["misc", "article"])

    # Specific tag (multi-word, descriptive)
    if "ai" in content or "artificial intelligence" in content:
        specific_tag = "artificial intelligence"
    elif "climate" in content or "environment" in content:
        specific_tag = "climate change"
    elif "design" in content or "apple" in content:
        specific_tag = "product design"
    else:
        specific_tag = "general topic"

    # Ensure unique tags and at least 3
    tags = list(set(general_tags[:2] + [specific_tag]))
    if len(tags) < 3:
        tags.append("content")
    logging.info(f"Generated tags for '{title}': {tags}")
    return tags


def fetch_articles_to_tag():
    """Fetch articles with fewer than 3 tags."""
    logging.info("Fetching articles with fewer than 3 tags...")
    all_articles = {}
    offset = 0
    count = 20  # Reduced batch size
    retries = 5

    while True:
        for attempt in range(retries):
            try:
                # Set timeout for API call
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(10)  # 10-second timeout
                response = pocket_instance.get(
                    count=count, offset=offset, detailType="complete", state="all"
                )
                signal.alarm(0)  # Disable timeout
                logging.info(f"Raw API response (offset={offset}): {response}")
                if not isinstance(response, tuple) or len(response) < 1:
                    logging.error(f"Invalid API response format: {response}")
                    raise ValueError(f"Invalid API response format: {response}")
                response_data = response[0]
                articles = response_data.get("list", {})
                if not isinstance(articles, dict):
                    logging.error(f"Unexpected 'list' format: {articles}")
                    raise ValueError(f"Unexpected 'list' format: {articles}")
                # Filter articles with fewer than 3 tags
                for item_id, article in articles.items():
                    if len(article.get("tags", {})) < 3:
                        all_articles[item_id] = article
                logging.info(
                    f"Fetched {len(articles)} articles at offset {offset}. Total to tag: {len(all_articles)}"
                )
                if len(articles) == 0:
                    logging.info(
                        f"No more articles to fetch. Total to tag: {len(all_articles)}"
                    )
                    return all_articles
                offset += count
                time.sleep(3)
                break
            except pocket.RateLimitException as e:
                delay = 120 * (attempt + 1)
                logging.warning(f"Rate limit hit: {str(e)}. Retrying in {delay}s...")
                print(f"Rate limit hit. Waiting {delay} seconds before retrying...")
                time.sleep(delay)
            except TimeoutError as e:
                signal.alarm(0)
                logging.error(f"Timeout at offset {offset}: {str(e)}")
                raise
            except Exception as e:
                delay = 5 * (attempt + 1)
                logging.error(
                    f"Pocket API error (attempt {attempt + 1}/{retries}, offset={offset}): {str(e)}",
                    exc_info=True,
                )
                time.sleep(delay)
                if "401" in str(e) or "403" in str(e):
                    logging.error(
                        "Authentication or permission error. Check POCKET_CONSUMER_KEY and POCKET_ACCESS_TOKEN."
                    )
                    raise
        else:
            logging.error(
                f"Failed to fetch articles after {retries} attempts at offset {offset}."
            )
            raise ValueError(f"Failed to fetch articles after {retries} attempts.")


def get_existing_tags(articles):
    """Get all existing tags and their article counts."""
    tag_counts = defaultdict(int)
    for item_id, article in articles.items():
        for tag in article.get("tags", {}):
            tag_counts[tag] += 1
    logging.info(f"Existing tags: {dict(tag_counts)}")
    return tag_counts


def tag_articles(articles):
    """Tag articles with at least 3 tags: 2 general (one-word), 1 specific (multi-word)."""
    existing_tags = get_existing_tags(articles)
    tagged_count = 0
    retries = 5

    for item_id, article in articles.items():
        current_tags = list(article.get("tags", {}).keys())
        if len(current_tags) >= 3:
            logging.info(
                f"Article {item_id} already has {len(current_tags)} tags: {current_tags}. Skipping."
            )
            continue

        title = article.get("resolved_title", article.get("given_title", ""))
        excerpt = article.get("excerpt", "")
        url = article.get("resolved_url", article.get("given_url", ""))
        logging.info(f"Processing article {item_id}: {title}")

        # Generate new tags
        new_tags = generate_tags_with_grok(title, excerpt, url)
        # Prefer existing tags to minimize single-article tags
        final_tags = []
        for tag in new_tags:
            # Use existing tag if similar and reusable (not single-article)
            for existing_tag, count in existing_tags.items():
                if tag.lower() in existing_tag.lower() and count > 1:
                    final_tags.append(existing_tag)
                    break
            else:
                final_tags.append(tag)
        # Ensure at least 3 tags
        final_tags = list(set(final_tags + current_tags))
        if len(final_tags) < 3:
            final_tags.append("content")
        if len(final_tags) < 3:
            final_tags.append("article")

        # Apply tags
        for attempt in range(retries):
            try:
                pocket_instance.tags_add(item_id, final_tags)
                logging.info(f"Added tags to article {item_id}: {final_tags}")
                tagged_count += 1
                # Update existing tags
                for tag in final_tags:
                    existing_tags[tag] += 1
                time.sleep(3)
                break
            except pocket.RateLimitException as e:
                delay = 120 * (attempt + 1)
                logging.warning(f"Rate limit hit: {str(e)}. Retrying in {delay}s...")
                print(f"Rate limit hit. Waiting {delay} seconds before retrying...")
                time.sleep(delay)
            except Exception as e:
                logging.error(f"Error tagging article {item_id}: {str(e)}")
                if "401" in str(e) or "403" in str(e):
                    print(
                        "Authentication or permission error. Regenerate POCKET_ACCESS_TOKEN."
                    )
                    raise
                break

    logging.info(f"Tagged {tagged_count} articles.")
    return tagged_count


def main():
    try:
        logging.info("Script started")
        logging.info(f"Consumer Key: {POCKET_CONSUMER_KEY[:10]}...")
        logging.info(f"Access Token: {POCKET_ACCESS_TOKEN[:10]}...")

        # Test Pocket API connectivity
        try:
            test_response = pocket_instance.get(
                count=1, detailType="complete", state="all"
            )
            logging.info(f"Pocket API test response: {test_response}")
            print("Pocket API connection successful.")
        except pocket.RateLimitException as e:
            logging.error(f"Rate limit exceeded: {str(e)}")
            print(
                "Pocket API rate limit exceeded. Please wait at least 1 hour and try again."
            )
            return
        except Exception as e:
            logging.error(f"Pocket API connectivity test failed: {str(e)}")
            print(f"Error connecting to Pocket API: {str(e)}.")
            return

        # Fetch articles to tag
        try:
            articles = fetch_articles_to_tag()
        except Exception as e:
            logging.error(f"Failed to fetch articles: {str(e)}")
            print(f"Error fetching articles: {str(e)}")
            return

        if not articles:
            logging.warning("No articles with fewer than 3 tags found.")
            print(
                "No articles need tagging. Verify your Pocket account at getpocket.com."
            )
            return

        # Tag articles
        tagged_count = tag_articles(articles)
        print(f"Tagged {tagged_count} articles with at least 3 tags each.")

        logging.info("Script finished")
        print("Script finished")
    except KeyboardInterrupt:
        logging.info("Script interrupted by user")
        print("Script stopped by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
