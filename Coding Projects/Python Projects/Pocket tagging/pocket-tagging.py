import requests

# Replace with your Pocket API consumer key and access token
CONSUMER_KEY = "105963-2f8fe9284c7d69f5fc0ee69"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

# Pocket API URLs
RETRIEVE_URL = "https://getpocket.com/v3/get"
MODIFY_URL = "https://getpocket.com/v3/send"

# Retrieve all items from the user's Pocket list
params = {
    "consumer_key": CONSUMER_KEY,
    "access_token": ACCESS_TOKEN,
    "detailType": "simple",
}
response = requests.post(RETRIEVE_URL, params=params)
data = response.json()

# Iterate over each item in the user's Pocket list
for item_id, item in data["list"].items():
    # Define the tags you want to add
    tags = ["tag1", "tag2", "tag3"]

    # Prepare the data for the modify request
    actions = [{"action": "tags_add", "item_id": item_id, "tags": ",".join(tags)}]
    params = {
        "consumer_key": CONSUMER_KEY,
        "access_token": ACCESS_TOKEN,
        "actions": actions,
    }

    # Send the modify request to add the tags
    response = requests.post(MODIFY_URL, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        print(f"Successfully added tags to item {item_id}")
    else:
        print(f"Failed to add tags to item {item_id}")
