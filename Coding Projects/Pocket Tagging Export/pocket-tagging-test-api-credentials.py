from pocket import Pocket
from dotenv import load_dotenv
import os

load_dotenv()
consumer_key = os.getenv("POCKET_CONSUMER_KEY")
access_token = os.getenv("POCKET_ACCESS_TOKEN")

if not consumer_key or not access_token:
    print("Error: Missing credentials in .env")
    exit(1)

pocket = Pocket(consumer_key=consumer_key, access_token=access_token)

try:
    response = pocket.get(count=1)
    print("Response type:", type(response))
    print("Response content:", response)
except Exception as e:
    print("Error:", str(e))
