from google.cloud import speech

client = speech.SpeechClient()

audio = speech.RecognitionAudio(
    uri="gs://cloud-samples-tests/speech/Google_Gnome.wav"
)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US",
    model="video", # Chosen model
)

operation = client.long_running_recognize(config=config, audio=audio)

print("Waiting for operation to complete...")
response = operation.result(timeout=90)

for i, result in enumerate(response.results):
    alternative = result.alternatives[0]
    print("-" \* 20)
    print(f"First alternative of result {i}")
    print(f"Transcript: {alternative.transcript}")
