import os
from dotenv import load_dotenv
from pocket import Pocket

print("Script started")

# Load environment variables
load_dotenv()
consumer_key = os.getenv("POCKET_CONSUMER_KEY")
access_token = os.getenv("POCKET_ACCESS_TOKEN")

if not consumer_key or not access_token:
    print("Error: Missing POCKET_CONSUMER_KEY or POCKET_ACCESS_TOKEN in .env")
    exit(1)

try:
    # Initialize Pocket API
    print("Initializing Pocket API...")
    pocket_instance = Pocket(consumer_key, access_token)

    # Example: Tag a small test set
    article_tags = [
        ("879442011", ["test1"]),
        ("3067648576", ["test2"]),
    ]
    print(f"Preparing to tag {len(article_tags)} articles")

    for item_id, tags in article_tags:
        print(f"Tagging item {item_id} with tags {tags}")
        pocket_instance.tags_add(item_id, tags)
        print(f"Finished tagging item {item_id}")

    print("Script finished successfully")

except Exception as e:
    print(f"An error occurred: {e}")
