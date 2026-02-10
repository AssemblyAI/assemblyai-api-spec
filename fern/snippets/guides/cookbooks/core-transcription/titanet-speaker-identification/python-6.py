elon_fingerprint = download_and_convert_to_wav(
    "https://api.assemblyai-solutions.com/storage/v1/object/sign/sam_training_bucket/musk_fingerprinting.wav?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzYW1fdHJhaW5pbmdfYnVja2V0L211c2tfZmluZ2VycHJpbnRpbmcud2F2IiwiaWF0IjoxNzAwNDM4OTAwLCJleHAiOjE3MzE5NzQ5MDB9.O3QOJSBqFNb1sg4nurwSFA13xIPHyKuon3UfHcFYit0&t=2023-11-20T00%3A08%3A20.071Z"
)
altman_fingerprint = download_and_convert_to_wav(
    "https://api.assemblyai-solutions.com/storage/v1/object/sign/sam_training_bucket/sam_altman_fingerprint.mp3?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzYW1fdHJhaW5pbmdfYnVja2V0L3NhbV9hbHRtYW5fZmluZ2VycHJpbnQubXAzIiwiaWF0IjoxNzAwNjY5NjI0LCJleHAiOjE3MzIyMDU2MjR9._1yuMGzBhFcHr7xv76160Hb_SC-mH_Wv3_qX-S7XsTU&t=2023-11-22T16%3A13%3A44.103Z"
)
lex_fingerprint = download_and_convert_to_wav(
    "https://api.assemblyai-solutions.com/storage/v1/object/sign/sam_training_bucket/lex_fridman_fingerprint.mp3?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzYW1fdHJhaW5pbmdfYnVja2V0L2xleF9mcmlkbWFuX2ZpbmdlcnByaW50Lm1wMyIsImlhdCI6MTcwMDY2OTc4OSwiZXhwIjoxNzMyMjA1Nzg5fQ.PUWTOLIHl4dcrWjh2ZJ_2TBaxMXpcU-x6OcvUDe6ZXQ&t=2023-11-22T16%3A16%3A29.697Z"
)

known_speakers = {"Elon Musk": elon_fingerprint, "Sam Altman": altman_fingerprint, "Lex Fridman": lex_fingerprint}

# Upload the known speakers.
for speaker, audio_file in known_speakers.items():
    print("***")
    print(speaker)
    print(audio_file)
    embedding = speaker_model.get_embedding(audio_file)
    add_speaker_embedding_to_pinecone(speaker, embedding)
