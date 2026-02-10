const data = {
  transcript_ids: [transcript_id],
  prompt: prompt,
  final_model: final_model,
  max_output_size: 1000,
};

const result = await axios.post(
  "https://api.assemblyai.com/lemur/v3/generate/task",
  data,
  { headers }
);
