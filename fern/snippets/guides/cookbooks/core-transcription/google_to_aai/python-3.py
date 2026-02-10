audio = speech.RecognitionAudio(uri="gs://cloud-samples-tests/speech/Google_Gnome.wav")

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US",
    model="video", # Chosen model
)

operation = client.long_running_recognize(config=config, audio=audio)
