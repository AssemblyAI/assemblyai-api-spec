transcripts = transcribe([
    '', # TODO ADD URLS
])

embeddings = create_transcripts_embeddings(transcripts)

qa_results = transcripts.lemur.question(questions).response

print(f"Question: {qa_results[0].question}")
print(f"Answer: {qa_results[0].answer}")
print()
get_citations(qa_results[0].question + ' ' + qa_results[0].answer)
