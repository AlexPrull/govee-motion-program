import requests
import uuid

API_KEY = "a53f7b0f-e2a2-4404-ab31-9fcb22389946"
device = "0E:7B:DA:B9:85:46:38:25"
model = "H612D"

url = "https://openapi.api.govee.com/router/api/v1/device/scenes"
headers = {
    "Govee-API-Key": API_KEY,
    "Content-Type": "application/json",
}

body = {
    "requestId": str(uuid.uuid4()),
    "payload": {"device": device, "sku": model}
}

response = requests.post(url, headers=headers, json=body)
print(response.json())