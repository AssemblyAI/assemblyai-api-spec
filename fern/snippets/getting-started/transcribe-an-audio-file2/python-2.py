with open("./example.mp3", "rb") as f:
    response = requests.post(base_url + "/v2/upload", headers=headers, data=f)

    if response.status_code != 200:
        print(f"Error: {response.status_code}, Response: {response.text}")
        response.raise_for_status()

    upload_json = response.json()
    audio_file = upload_json["upload_url"]
