audio_file = "audio.wav" # your local file path
transcript: aai.Transcript = transcribe_audio(audio_file, language="hr") # select a language code
transcript_with_speakers = get_speaker_labels(audio_file, transcript)
print(transcript_with_speakers)
