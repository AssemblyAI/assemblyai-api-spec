transcripts = transcribe([
    '', # TODO ADD URLS
])

embeddings = create_transcripts_embeddings(transcripts, granularity='sentence')

qa_results = transcripts.lemur.question(questions).response

print(f"Question: {qa_results[0].question}")
print(f"Answer: {qa_results[0].answer}")
print()

pain_point_array = json.loads(qa_results[0].answer.strip())
for pp in pain_point_array:
    print('Pain Point:', pp)
    get_examples(pp)
