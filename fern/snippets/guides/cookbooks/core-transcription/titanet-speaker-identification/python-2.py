from pinecone import Pinecone, ServerlessSpec

# Obtain from your Pinecone dashboard.
pc = Pinecone(api_key="PINECONE_KEY_HERE")

pc.create_index(
    name="speaker-embeddings",
    dimension=192,  # Replace with model-specific dimensions - 192 is for TitaNet-Large.
    metric="cosine",  # Replace with your model metric.
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1",
    ),
)

# Connect to our new index.
index = pc.Index("speaker-embeddings")
