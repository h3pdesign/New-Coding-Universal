import os
from pocket import Pocket
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists, optional here)
load_dotenv()

# Pocket consumer key (replace with yours or load from .env)
POCKET_CONSUMER_KEY = os.getenv("POCKET_CONSUMER_KEY") or "your_consumer_key_here"
REDIRECT_URI = "http://localhost"  # Placeholder for desktop apps


def get_access_token():
    # Initialize Pocket with consumer key only for auth flow
    pocket = Pocket(consumer_key=POCKET_CONSUMER_KEY)

    try:
        # Step 1: Get a request token
        request_token = pocket.get_request_token(redirect_uri=REDIRECT_URI)
        print(f"Request token: {request_token}")

        # Step 2: Generate the authorization URL
        auth_url = pocket.get_auth_url(code=request_token)
        print(f"Please visit this URL to authorize the app: {auth_url}")
        print("Log in to Pocket, authorize the app, then press Enter here...")

        # Wait for user to authorize in browser
        input()

        # Step 3: Convert request token to access token
        access_token = pocket.get_access_token(request_token)
        print(f"Your new access token is: {access_token}")
        print(f"Update your .env file with: POCKET_ACCESS_TOKEN={access_token}")
        return access_token

    except Exception as e:
        print(f"Error during authentication: {str(e)}")
        return None


if __name__ == "__main__":
    # Ensure consumer key is set
    if not POCKET_CONSUMER_KEY or "your_consumer_key_here" in POCKET_CONSUMER_KEY:
        print("Please set POCKET_CONSUMER_KEY in .env or replace it in the code.")
        print("Get it from https://getpocket.com/developer/apps/")
    else:
        get_access_token()
