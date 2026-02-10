from openai import OpenAI

api_key = "YOUR_OPENAI_API_KEY"
client = OpenAI(api_key)

audio_file = open("./example.wav", "rb")

transcript = client.audio.transcriptions.create(
    model = "whisper-1",
    file = audio_file
)

print(transcript.text)
