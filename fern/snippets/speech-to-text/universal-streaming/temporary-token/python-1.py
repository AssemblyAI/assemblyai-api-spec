import requests
from urllib.parse import urlencode

url = "https://streaming.assemblyai.com/v3/token"
response = requests.get(
    f"{url}?{urlencode({'expires_in_seconds': 60})}",
    headers={"Authorization": "<YOUR_API_KEY>"}
)
data = response.json()
return data.get("token")
