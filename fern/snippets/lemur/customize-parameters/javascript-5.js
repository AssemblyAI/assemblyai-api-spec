const data = {
  transcript_ids: [id1, id2, id3],
  prompt: prompt,
  final_model: final_model,
};

const result = await axios.post(
  "https://api.assemblyai.com/lemur/v3/generate/task",
  data,
  { headers }
);
