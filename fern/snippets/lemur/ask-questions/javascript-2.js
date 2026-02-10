import axios from "axios";

// Step 1: Transcribe the audio
const base_url = "https://api.assemblyai.com";
const headers = { authorization: "<YOUR_API_KEY>" };

const audio_url = "https://assembly.ai/meeting.mp4";
const data = { audio_url };

const response = await axios.post(base_url + "/v2/transcript", data, {
  headers,
});
const transcript_id = response.data.id;
const polling_endpoint = base_url + `/v2/transcript/${transcript_id}`;

let transcript;
while (true) {
  transcript = (await axios.get(polling_endpoint, { headers })).data;
  if (transcript.status === "completed") break;
  if (transcript.status === "error")
    throw new Error(`Transcription failed: ${transcript.error}`);
  await new Promise((resolve) => setTimeout(resolve, 3000));
}

// Step 2: Create structured Q&A prompt
const questions = [
  "What are the top level KPIs for engineering? (KPI stands for key performance indicator)",
  "How many days has it been since the data team has gotten updated metrics? (Choose from: 1, 2, 3, 4, 5, 6, 7, more than 7)",
];

const prompt = `Answer the following questions based on the meeting transcript. Format your response as:
Q1: [question]
A1: [answer]
Q2: [question] 
A2: [answer]

Questions:
${questions.map((q, i) => `${i + 1}. ${q}`).join("\n")}

Context: This is a GitLab meeting to discuss logistics.`;

// Step 3: Send to LLM Gateway
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
console.log(result.data.choices[0].message.content);
