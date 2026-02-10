data = {
    "audio_url": upload_url, # You can also use a URL to an audio or video file on the web
    "redact_pii": True,
    "redact_pii_policies": ["person_name", "organization", "occupation"],
    "redact_pii_sub": "hash",
    "redact_pii_audio": True,
    "redact_pii_audio_quality": "wav" # Optional. Defaults to "mp3"
}

# ...
redacted_audio_polling_endpoint = base_url + "/v2/transcript/" + transcript_id + "/redacted-audio"

while True:
    redacted_audio_result = requests.get(redacted_audio_polling_endpoint, headers=headers).json()

    if redacted_audio_result['status'] == 'redacted_audio_ready':
        print(redacted_audio_result['redacted_audio_url'])
        break
    elif redacted_audio_result['status'] == 'error':
        raise RuntimeError(f"Transcription failed: {redacted_audio_result['error']}")
    else:
        time.sleep(3)
