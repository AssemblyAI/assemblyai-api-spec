# Local Files
with open("./my-audio.mp3", "rb") as f:
    files = {"audio": ("my-audio.mp3", f, "audio/mp3")}
    response = requests.post(base_url + "/v2/upload",
                            headers=headers,
                            files=files)

upload_url = response.json()["audio_url"]

data = {
    "audio_url": upload_url
}

#Public URLs
audio_file = "https://assembly.ai/sports_injuries.mp3"

data = {
    "audio_url": audio_file
}
