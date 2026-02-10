const { response, request_id } = await client.lemur.task({
  transcript_ids: [transcript.id],
  prompt,
});

const deletionResponse = await client.lemur.purgeRequestData(request_id);
