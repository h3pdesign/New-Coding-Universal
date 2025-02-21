import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Pocket API credentials
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY")
POCKET_ACCESS_TOKEN = os.getenv("POCKET_ACCESS_TOKEN")

# Validate environment variables
if not all([POCKET_CONSUMER_KEY, POCKET_ACCESS_TOKEN]):
    raise ValueError("Missing required environment variables. Check your .env file.")

# Define the action
action = [{"action": "tags_add", "item_id": "3433414518", "tags": "test1,test2"}]

# Prepare the payload
payload = {
    "consumer_key": POCKET_CONSUMER_KEY,
    "access_token": POCKET_ACCESS_TOKEN,
    "actions": action,
}

# Send the request directly to Pocket's API
url = "https://getpocket.com/v3/send"
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
    response.raise_for_status()
    print("Test tag applied successfully")
    print("Response:", response.json())
except requests.exceptions.HTTPError as e:
    print(f"Error tagging: {e}")
    print(f"Response status: {e.response.status_code}")
    print(f"Response details: {e.response.text}")
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")

# Verify the tags
try:
    verify_url = "https://getpocket.com/v3/get"
    verify_payload = {
        "consumer_key": POCKET_CONSUMER_KEY,
        "access_token": POCKET_ACCESS_TOKEN,
        "item_id": "3433414518",
    }
    verify_response = requests.post(
        verify_url, data=json.dumps(verify_payload), headers=headers, timeout=10
    )
    verify_response.raise_for_status()
    result = verify_response.json()
    tags = result["list"].get("3433414518", {}).get("tags", {})
    print("Verification:", tags)
except requests.exceptions.RequestException as e:
    print(f"Verification error: {e}")
