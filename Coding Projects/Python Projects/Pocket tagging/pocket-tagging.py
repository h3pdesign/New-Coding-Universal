import requests
import json
import re

# Replace the following variables with your own Pocket API credentials
consumer_key = "your_consumer_key"
access_token = "your_access_token"

# Get all items from the account
get_url = "https://getpocket.com/v3/get"
get_params = {
    "consumer_key": consumer_key,
    "access_token": access_token,
    "state": "all",
    "detailType": "complete",
}
response = requests.post(get_url, json=get_params)
items = json.loads(response.text)["list"]

# Add tags to each item
for item_id in items:
    item = items[item_id]
    title = item["resolved_title"]
    tags = set(re.findall(r"\b\w+\b", title)) - {
        "a",
        "an",
        "the",
        "and",
        "or",
        "not",
        "for",
        "in",
        "on",
        "at",
        "to",
        "of",
        "with",
        "by",
        "from",
        "is",
        "are",
        "was",
        "were",
        "this",
        "that",
        "these",
        "those",
        "my",
        "your",
        "his",
        "her",
        "its",
        "our",
        "their",
        "i",
        "you",
        "he",
        "she",
        "it",
        "we",
        "they",
    }
    tags = list(tags)[:6]
    item_url = "https://getpocket.com/v3/send"
    item_params = {
        "consumer_key": consumer_key,
        "access_token": access_token,
        "actions": [{"action": "tags_add", "item_id": item_id, "tags": ",".join(tags)}],
    }
    response = requests.post(item_url, json=item_params)

print("All items have been tagged with generated tags")
