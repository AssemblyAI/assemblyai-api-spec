const { response } = await client.lemur.task({
  prompt,
  transcript_ids: [transcript.id],
  final_model,
  temperature: 0.7,
});
