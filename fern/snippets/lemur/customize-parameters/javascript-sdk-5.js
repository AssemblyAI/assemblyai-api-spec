const { response } = await client.lemur.task({
  transcript_ids: [id1, id2, id3],
  prompt: "Provide a summary of these customer calls.",
});
