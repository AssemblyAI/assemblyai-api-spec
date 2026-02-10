const { response } = await client.lemur.task({
  prompt,
  transcript_ids: [transcript.id],
  final_model,
  max_output_size: 1000,
});
