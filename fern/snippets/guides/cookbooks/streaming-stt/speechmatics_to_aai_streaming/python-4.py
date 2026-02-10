import requests

def generate_temp_token(api_key, ttl=60):
    """Generate a temporary authentication token that expires after the specified time."""
    url = "https://mp.speechmatics.com/v1/api_keys?type=rt"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "ttl": ttl
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    return data.get("key_value")
