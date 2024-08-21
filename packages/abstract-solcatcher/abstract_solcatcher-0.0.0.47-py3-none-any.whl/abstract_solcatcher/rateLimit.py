from abstract_database import *
from abstract_apis import *
import requests
# Base URL for your Flask app

# 1. Call the /rate_limit endpoint
def get_rate_limit_url(method_name):
    url = get_url(getSolcatcherUrl(),'rate_limit')
    response = requests.get(url, params={"method": method_name})
    if response.status_code == 200:
        data = response.json()
        return data.get("url")
    else:
        print(f"Failed to get rate limit URL: {response.status_code}")
        return None
# 2. Call the /log_response endpoint
def log_response(method_name, response_data={}):
    payload = {
        "method": method_name,
        "response_data": response_data
    }
    url = get_url(getSolcatcherUrl(),'log_response')
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Response logged successfully.")
    else:
        print(f"Failed to log response: {response.status_code}")
