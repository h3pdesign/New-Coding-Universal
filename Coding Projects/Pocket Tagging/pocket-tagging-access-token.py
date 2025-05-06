import os
import requests
import json
from dotenv import load_dotenv, set_key

# Configure logging
import logging

logging.basicConfig(
    filename="pocket_auth.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def load_env():
    """Load environment variables from .env file."""
    load_dotenv()
    consumer_key = os.getenv("POCKET_CONSUMER_KEY")
    if not consumer_key:
        logging.error("POCKET_CONSUMER_KEY not found in .env file.")
        raise ValueError("POCKET_CONSUMER_KEY is required in .env file.")
    return consumer_key


def get_request_token(consumer_key, redirect_uri="http://localhost:8000/callback"):
    """Request a temporary request token from Pocket."""
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "X-Accept": "application/json",
    }
    payload = {"consumer_key": consumer_key, "redirect_uri": redirect_uri}
    try:
        response = requests.post(
            "https://getpocket.com/v3/oauth/request",
            headers=headers,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        request_token = response.json().get("code")
        if not request_token:
            logging.error("No request token received from Pocket API.")
            raise ValueError("Failed to obtain request token.")
        logging.info(f"Received request token: {request_token}")
        return request_token
    except requests.exceptions.RequestException as e:
        logging.error(f"Error requesting request token: {str(e)}")
        raise Exception(f"Error requesting request token: {str(e)}")


def get_authorization_url(request_token, redirect_uri):
    """Generate the URL for user authorization."""
    return f"https://getpocket.com/auth/authorize?request_token={request_token}&redirect_uri={redirect_uri}"


def get_access_token(consumer_key, request_token):
    """Exchange the request token for an access token."""
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "X-Accept": "application/json",
    }
    payload = {"consumer_key": consumer_key, "code": request_token}
    try:
        response = requests.post(
            "https://getpocket.com/v3/oauth/authorize",
            headers=headers,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        access_token = response.json().get("access_token")
        username = response.json().get("username")
        if not access_token:
            logging.error("No access token received from Pocket API.")
            raise ValueError("Failed to obtain access token.")
        logging.info(f"Received access token for user: {username}")
        return access_token
    except requests.exceptions.RequestException as e:
        logging.error(f"Error requesting access token: {str(e)}")
        raise Exception(f"Error requesting access token: {str(e)}")


def update_env_file(access_token):
    """Update the .env file with the new access token."""
    env_file = ".env"
    try:
        set_key(env_file, "POCKET_ACCESS_TOKEN", access_token)
        logging.info("Updated .env file with POCKET_ACCESS_TOKEN.")
        print("Access token successfully saved to .env file.")
    except Exception as e:
        logging.error(f"Error updating .env file: {str(e)}")
        raise Exception(f"Error updating .env file: {str(e)}")


def main():
    print("Starting Pocket access token generation...")
    logging.info("Starting Pocket access token generation...")

    # Load consumer key from .env
    try:
        consumer_key = load_env()
    except ValueError as e:
        print(str(e))
        return

    # Set redirect URI (placeholder for testing)
    redirect_uri = "http://localhost:8000/callback"

    # Step 1: Get request token
    try:
        request_token = get_request_token(consumer_key, redirect_uri)
        print(f"Request Token: {request_token}")
    except Exception as e:
        print(str(e))
        return

    # Step 2: Prompt user to authorize the app
    auth_url = get_authorization_url(request_token, redirect_uri)
    print("\nPlease complete the following steps:")
    print(f"1. Open this URL in your browser: {auth_url}")
    print("2. Log in to Pocket and authorize the app.")
    print(
        "3. After authorization, you may see an error (e.g., 'localhost not found'). This is normal."
    )
    print("4. Return here and press Enter to continue.")
    input("Press Enter after authorizing...")

    # Step 3: Get access token
    try:
        access_token = get_access_token(consumer_key, request_token)
        print(f"Access Token: {access_token}")
    except Exception as e:
        print(str(e))
        return

    # Step 4: Update .env file
    try:
        update_env_file(access_token)
    except Exception as e:
        print(str(e))
        return

    print("\nSuccess! Your .env file now includes the POCKET_ACCESS_TOKEN.")
    print("You can now run your Pocket tagging script.")
    logging.info("Pocket access token generation completed successfully.")


if __name__ == "__main__":
    main()
