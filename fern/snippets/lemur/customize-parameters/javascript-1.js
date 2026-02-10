const data = {
  prompt: prompt,
  transcript_ids: [transcript_id],
  final_model: "anthropic/claude-sonnet-4-20250514",
};

const result = await axios.post(
  "https://api.assemblyai.com/lemur/v3/generate/task",
  data,
  { headers }
);
