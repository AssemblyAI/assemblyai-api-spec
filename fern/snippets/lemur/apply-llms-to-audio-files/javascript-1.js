import axios from "axios";
import fs from "fs-extra";

// Step 1: Transcribe the audio
const base_url = "https://api.assemblyai.com";

const headers = {
  authorization: "<YOUR_API_KEY>",
};

const path = "./my-audio.mp3";
const audioData = await fs.readFile(path);
const uploadResponse = await axios.post(`${base_url}/v2/upload`, audioData, {
  headers,
});

const uploadUrl = uploadResponse.data.upload_url;

const data = {
  audio_url: uploadUrl, // You can also use a URL of an audio or video file on the web
};

const response = await axios.post(base_url + "/v2/transcript", data, {
  headers,
});

const transcript_id = response.data.id;
const polling_endpoint = base_url + `/v2/transcript/${transcript_id}`;

let transcript;
while (true) {
  transcript = (await axios.get(polling_endpoint, { headers })).data;

  if (transcript.status === "completed") {
    break;
  } else if (transcript.status === "error") {
    throw new Error(`Transcription failed: ${transcript.error}`);
  } else {
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}

// Step 2: Send transcript to LLM Gateway
const prompt = "Provide a brief summary of the transcript.";

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
