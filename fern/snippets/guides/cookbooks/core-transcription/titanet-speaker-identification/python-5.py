import torch
import numpy as np
import uuid


def add_speaker_embedding_to_pinecone(speaker_name, speaker_embedding, unique_id=None):
    # Ensure the embedding is a 1D numpy array.
    if isinstance(speaker_embedding, torch.Tensor):
        embedding_np = speaker_embedding.squeeze().cpu().numpy()
    elif isinstance(speaker_embedding, np.ndarray):
        embedding_np = speaker_embedding.squeeze()
    else:
        raise ValueError("Unsupported embedding type. Expected torch.Tensor or numpy.ndarray")

    # Ensure the embedding is the correct shape
    if embedding_np.shape != (192,):
        raise ValueError(f"Expected embedding of shape (192,), but got {embedding_np.shape}")

    # Convert to list for Pinecone
    embedding_list = embedding_np.tolist()

    # Generate a unique ID if not provided
    if unique_id is None:
        unique_id = f"speaker_{speaker_name}_{uuid.uuid4().hex[:8]}"

    # Create the metadata dictionary
    metadata = {"speaker_name": speaker_name}

    # Upsert the vector to Pinecone
    upsert_response = index.upsert(vectors=[(unique_id, embedding_list, metadata)])

    print(f"Upserted embedding for speaker {speaker_name} with ID {unique_id}")
    return unique_id
