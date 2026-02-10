const headers = {
  authorization: "<YOUR_API_KEY>",
  "Content-Type": "application/json",
};

const conversation_history = [
  { role: "user", content: "What is the capital of France?" },
  { role: "assistant", content: "The capital of France is Paris." },
  { role: "user", content: "What's the population?" },
];

fetch("https://llm-gateway.assemblyai.com/v1/chat/completions", {
  method: "POST",
  headers: headers,
  body: JSON.stringify({
    model: "claude-sonnet-4-5-20250929",
    messages: conversation_history,
    max_tokens: 1000,
  }),
})
  .then((response) => response.json())
  .then((result) => {
    const agent_response = result.choices[0].message.content;
    console.log(agent_response);

    // Append the assistant's response to conversation history
    conversation_history.push({ role: "assistant", content: agent_response });
  })
  .catch((error) => {
    console.error("Error:", error);
  });
