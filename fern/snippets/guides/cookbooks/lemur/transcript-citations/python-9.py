# Embed the LLM output
llm_gateway_embedding = embedder.encode(llm_answer)

# Vectorize transcript embeddings
np_embeddings = np.array(list(embeddings.values()))
metadata = list(embeddings.keys())

# Find the top 3 most similar quotes
print("Finding matching quotes in transcript...")
knn = NearestNeighbors(n_neighbors=3, metric="cosine")
knn.fit(np_embeddings)
distances, indices = knn.kneighbors([llm_gateway_embedding])

matches = []
for distance, index in zip(distances[0], indices[0]):
    result_metadata = metadata[index]
    matches.append(
        {
            "start_timestamp": result_metadata[0],
            "end_timestamp": result_metadata[1],
            "transcript_id": result_metadata[2],
            "text": result_metadata[3],
            "confidence": 1 - distance,
        }
    )

# Display results
print("\n" + "="*80)
print("BEST MATCHING QUOTES FROM TRANSCRIPT:")
print("="*80 + "\n")

for index, m in enumerate(matches):
    print('QUOTE #{}: "{}"'.format(index + 1, m['text']))
    print('START TIMESTAMP:', str(datetime.timedelta(seconds=m['start_timestamp']/1000)))
    print('END TIMESTAMP:', str(datetime.timedelta(seconds=m['end_timestamp']/1000)))
    print('CONFIDENCE:', m['confidence'])
    print()
