import numpy as np
from sklearn.neighbors import NearestNeighbors
import openai

# Set up OpenAI API key
openai.api_key = "YOUR_OPENAI_TOKEN"

def embed_block(block_text):
    # Embed the block of text using OpenAI embeddings
    embedding = openai.Embedding.create(
        input=block_text,
        model='text-embedding-ada-002',
    ).to_dict()['data'][0]['embedding']

    # Store the embedding with the timestamp in the dictionary
    return embedding

def find_relevant_matches(embedded_blocks, new_block_text, k=3):
    matches = []
    # Embed the new block of text using OpenAI embeddings
    new_embedding = embed_block(new_block_text)

    # Prepare the embeddings for the KNN search
    embeddings = np.array(list(embedded_blocks.values()))
    metadata = list(embedded_blocks.keys())

    # Perform KNN search to find the most relevant matches
    knn = NearestNeighbors(n_neighbors=k)
    knn.fit(embeddings)
    distances, indices = knn.kneighbors([new_embedding])

    # Print the relevant matches
    # print(f"Relevant Matches for '{new_block_text}':")
    for distance, index in zip(distances[0], indices[0]):
        result_metadata = metadata[index]
        # print(f"Timestamp: {timestamp}, Similarity: {1-distance:.4f}")
        # print(f"Block Text: {embedded_blocks[timestamp]}")
        # print()
        matches.append({
            'timestamp': result_metadata[0],
            'transcript_id': result_metadata[1],
            'text': result_metadata[2],
            'confidence': 1-distance
        })
    return matches
