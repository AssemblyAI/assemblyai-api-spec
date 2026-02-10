# Initialize embedder
embedder = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
embeddings = {}

# Create sliding window of sentences and generate embeddings
print("Creating embeddings...")
sentence_groups = sliding_window(sentences, 5, 2)

for sentence_group in sentence_groups:
    combined_text = " ".join([sentence["text"] for sentence in sentence_group])
    start = sentence_group[0]["start"]
    end = sentence_group[-1]["end"]

    embeddings[(start, end, transcript_id, combined_text)] = embedder.encode(combined_text)
