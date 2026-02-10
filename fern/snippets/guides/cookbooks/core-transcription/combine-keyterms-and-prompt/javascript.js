import axios from "axios";

const baseUrl = "https://api.assemblyai.com";
const headers = {
  authorization: "<YOUR_API_KEY>",
};

// Define your base prompt and keyterms
const basePrompt = "This is a YouTube video describing common sports injuries.";
const keyterms = [
  "Sprained ankle",
  "ACL tear",
  "Hamstring strain",
  "Rotator cuff injury",
  "Tennis elbow",
  "Shin splints",
  "Concussion",
  "Groin pull",
  "Achilles tendonitis",
  "Meniscus tear",
];

// Append context with keyterms to the prompt
const promptWithContext = `${basePrompt}\n\nContext: ${keyterms.join(",")}`;

const data = {
  audio_url: "https://assembly.ai/sports_injuries.mp3",
  speech_models: ["universal-3-pro"],
  language_detection: true,
  prompt: promptWithContext,
};

const url = `${baseUrl}/v2/transcript`;
const response = await axios.post(url, data, { headers: headers });

const transcriptId = response.data.id;
const pollingEndpoint = `${baseUrl}/v2/transcript/${transcriptId}`;

while (true) {
  const pollingResponse = await axios.get(pollingEndpoint, {
    headers: headers,
  });
  const transcriptionResult = pollingResponse.data;

  if (transcriptionResult.status === "completed") {
    console.log(transcriptionResult.text);
    break;
  } else if (transcriptionResult.status === "error") {
    throw new Error(`Transcription failed: ${transcriptionResult.error}`);
  } else {
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}
