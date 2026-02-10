const response = await fetch(
  "https://llm-gateway.assemblyai.com/v1/chat/completions",
  {
    method: "POST",
    headers: {
      authorization: "<YOUR_API_KEY>",
      "content-type": "application/json",
    },
    body: JSON.stringify({
      model: "claude-sonnet-4-5-20250929",
      messages: [{ role: "user", content: "What is the capital of France?" }],
      max_tokens: 1000,
    }),
  }
);

const result = await response.json();
console.log(result.choices[0].message.content);
