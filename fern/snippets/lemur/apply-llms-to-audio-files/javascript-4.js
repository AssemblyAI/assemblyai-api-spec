const llm_gateway_data = {
  model: "claude-sonnet-4-5-20250929",
  messages: [
    { role: "user", content: `${prompt}\n\nTranscript: ${transcript.text}` },
  ],
  max_tokens: 1000,
};

const result = await axios.post(
  "https://llm-gateway.assemblyai.com/v1/chat/completions",
  llm_gateway_data,
  { headers }
);
