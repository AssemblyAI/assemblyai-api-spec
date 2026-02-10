audio_file = download_and_convert_to_wav(
    "https://api.assemblyai-solutions.com/storage/v1/object/sign/sam_training_bucket/musk_fingerprinting.wav?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1cmwiOiJzYW1fdHJhaW5pbmdfYnVja2V0L211c2tfZmluZ2VycHJpbnRpbmcud2F2IiwiaWF0IjoxNzAwNDM4OTAwLCJleHAiOjE3MzE5NzQ5MDB9.O3QOJSBqFNb1sg4nurwSFA13xIPHyKuon3UfHcFYit0&t=2023-11-20T00%3A08%3A20.071Z"
)
utterance_embedding = speaker_model.get_embedding(audio_file)

results = index.query(vector=utterance_embedding.tolist(), top_k=3, include_metadata=True)

print(results)
