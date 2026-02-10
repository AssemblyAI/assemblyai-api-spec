const { response } = await client.lemur.task({
  transcript_ids: [transcript.id],
  prompt,
});

console.log(response);
