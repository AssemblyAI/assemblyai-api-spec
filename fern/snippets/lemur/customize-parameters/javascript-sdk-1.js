const { response } = await client.lemur.task({
  transcript_ids: [transcript.id],
  prompt,
  final_model: "anthropic/claude-sonnet-4-20250514",
});
