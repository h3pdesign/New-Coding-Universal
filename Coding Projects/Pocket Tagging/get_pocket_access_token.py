import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file (optional if already set)
load_dotenv()

# Pocket consumer key
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY") or "your_consumer_key_here"
REDIRECT_URI = "http://localhost"  # Placeholder for desktop apps


def get_access_token():
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "X-Accept": "application/json",
    }

    try:
        # Step 1: Get a request token
        request_url = "https://getpocket.com/v3/oauth/request"
        payload = {"consumer_key": POCKET_CONSUMER_KEY, "redirect_uri": REDIRECT_URI}
        response = requests.post(request_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        request_token = response.json()["code"]
        print(f"Request token: {request_token}")

        # Step 2: Generate the authorization URL
        auth_url = f"https://getpocket.com/auth/authorize?request_token={request_token}&redirect_uri={REDIRECT_URI}"
        print(f"Please visit this URL to authorize the app: {auth_url}")
        print("Log in to Pocket, authorize the app, then press Enter here...")

        # Wait for user to authorize in browser
        input()

        # Step 3: Convert request token to access token
        authorize_url = "https://getpocket.com/v3/oauth/authorize"
        payload = {"consumer_key": POCKET_CONSUMER_KEY, "code": request_token}
        response = requests.post(
            authorize_url, json=payload, headers=headers, timeout=10
        )
        response.raise_for_status()
        access_token = response.json()["access_token"]
        print(f"Your new access token is: {access_token}")
        print(f"Update your .env file with: POCKET_ACCESS_TOKEN={access_token}")
        return access_token

    except requests.exceptions.HTTPError as e:
        print(f"Error during authentication: {e}")
        print(f"Response status: {e.response.status_code}")
        print(f"Response details: {e.response.text}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None
    except KeyError as e:
        print(f"Error parsing response: {e}")
        return None


if __name__ == "__main__":
    # Ensure consumer key is set
    if not POCKET_CONSUMER_KEY or "your_consumer_key_here" in POCKET_CONSUMER_KEY:
        print("Please set POCKET_CONSUMER_KEY in .env or replace it in the code.")
        print("Get it from https://getpocket.com/developer/apps/")
    else:
        get_access_token()
