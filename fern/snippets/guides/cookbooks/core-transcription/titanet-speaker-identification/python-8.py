from sklearn.metrics.pairwise import cosine_similarity


def find_closest_speaker(utterance_embedding, local_embeddings=None, local_only=False, threshold=0.5):
    def cosine_sim(a, b):
        return cosine_similarity(a.reshape(1, -1), b.reshape(1, -1))[0][0]

    best_match = {"speaker_name": "No match found", "score": 0}

    # Local embeddings processing.
    if local_embeddings is not None:
        for speaker_name, embedding in local_embeddings.items():
            score = cosine_sim(utterance_embedding, embedding)
            if score > best_match["score"]:
                print("Identified speaker " + speaker_name + " confidence " + str(score))
                best_match = {"speaker_name": speaker_name, "score": score}

    # Pinecone query (if not local_only and local_embeddings is empty or not provided)
    if not local_only and (local_embeddings is None or len(local_embeddings) == 0):
        results = index.query(vector=utterance_embedding.tolist(), top_k=1, include_metadata=True)
        if results["matches"]:
            pinecone_match = results["matches"][0]
            pinecone_score = pinecone_match["score"]
            if pinecone_score > best_match["score"]:
                best_match = {"speaker_name": pinecone_match["metadata"]["speaker_name"], "score": pinecone_score}

    # Check if the best match meets the threshold.
    if best_match["score"] < threshold:
        return "No match found", 0

    return best_match["speaker_name"], best_match["score"]
