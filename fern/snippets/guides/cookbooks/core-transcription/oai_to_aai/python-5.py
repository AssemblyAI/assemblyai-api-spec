transcript = client.audio.transcriptions.create(
    file = audio_file,
    prompt = "INSERT_PROMPT" # Optional text to guide the model's style
    language = "en" # Set language code
    model = "whisper-1",
    response_format = "verbose_json",
    timestamp_granularities = ["word"]
)

# Access word-level timestamps

print(transcript.words)
