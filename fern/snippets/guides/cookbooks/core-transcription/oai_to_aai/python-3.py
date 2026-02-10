client = OpenAI()

# Local Files

audio_file = open("./example.wav", "rb")
transcript = client.audio.transcriptions.create(
    model = "whisper-1",
    file = audio_file
)
