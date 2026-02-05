"""
Helper script to list all Govee devices associated with the API key.
Used during setup to discover device IDs, models (SKU), and capabilities.
Not used by the main automation runtime.
"""

import requests
from config import API_KEY

url = "https://openapi.api.govee.com/router/api/v1/user/devices"

headers = {
    "Govee-API-Key": API_KEY,
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print(response.status_code)
print(response.json())