audio_urls = [
    "https://storage.googleapis.com/aai-web-samples/public_benchmarking_portugese.mp3",
    "https://storage.googleapis.com/aai-web-samples/public_benchmarking_spanish.mp3",
    "https://storage.googleapis.com/aai-web-samples/slovenian_luka_doncic_interview.mp3",
    "https://storage.googleapis.com/aai-web-samples/5_common_sports_injuries.mp3",
]

for audio_url in audio_urls:
    language_code = detect_language(audio_url)
    print("Identified language:", language_code)

    transcript = transcribe_file(audio_url, language_code)
    print("Transcript:", transcript.text[:100], "...")
