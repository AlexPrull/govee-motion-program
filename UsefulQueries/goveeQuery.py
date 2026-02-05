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