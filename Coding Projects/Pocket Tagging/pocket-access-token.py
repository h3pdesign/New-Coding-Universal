import requests

# Replace with your actual consumer key from Pocket's developer portal
CONSUMER_KEY = "113137-db3d33cc63e9b9b4b028856"
REDIRECT_URI = "http://localhost"  # Placeholder for desktop apps


def get_access_token():
    # Step 1: Get a request token
    request_url = "https://getpocket.com/v3/oauth/request"
    payload = {"consumer_key": CONSUMER_KEY, "redirect_uri": REDIRECT_URI}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(request_url, json=payload, headers=headers)
        response.raise_for_status()
        request_token = response.text.split("code=")[1]
        print(f"Request token: {request_token}")

        # Step 2: Generate the authorization URL
        auth_url = f"https://getpocket.com/auth/authorize?request_token={request_token}&redirect_uri={REDIRECT_URI}"
        print(f"Please visit this URL to authorize the app: {auth_url}")

        # Wait for user to authorize
        print("After authorizing, press Enter to continue...")
        input()

        # Step 3: Convert request token to access token
        access_url = "https://getpocket.com/v3/oauth/authorize"
        payload = {"consumer_key": CONSUMER_KEY, "code": request_token}
        response = requests.post(access_url, json=payload, headers=headers)
        response.raise_for_status()
        access_token = response.text.split("access_token=")[1].split("&")[0]
        print(f"Your access token is: {access_token}")
        print("Save this token and use it in your pocket-tagging-grok.py script!")
        return access_token

    except requests.exceptions.RequestException as e:
        print(f"Error during authentication: {e}")
        return None


if __name__ == "__main__":
    access_token = get_access_token()
