transcriber = aai.Transcriber()
audio_url = ("https://api.assemblyai-solutions.com/storage/v1/object/public/dual-channel-phone-data/Fisher_Call_Centre/audio05851.wav")
config = aai.TranscriptionConfig(speaker_labels=True)
transcript = transcriber.transcribe(audio_url, config)

talk_listen_stats = calculate_talk_listen_ratios(transcript)
print(talk_listen_stats)
