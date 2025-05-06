import pocket

pocket_instance = pocket.Pocket(
    consumer_key="your_consumer_key", access_token="your_access_token"
)
try:
    response = pocket_instance.get(count=1, detailType="complete", state="all")
    print(response)
except pocket.RateLimitException as e:
    print(f"Rate limit error: {str(e)}")
except Exception as e:
    print(f"Error: {str(e)}")
