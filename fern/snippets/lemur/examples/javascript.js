import axios from "axios";

const base_url = "https://api.assemblyai.com";

const headers = {
  authorization: "<YOUR_API_KEY>",
};

// Step 1: Transcribe an audio file.
// import fs from 'fs-extra';
// const path = './my-audio.mp3';
// const audioData = await fs.readFile(path)
// const uploadResponse = await axios.post(`${baseUrl}/v2/upload`, audioData, {
// headers
// })
// const uploadUrl = uploadResponse.data.upload_url

// Or use a publicly-accessibly URL:
const uploadUrl = "https://assembly.ai/call.mp4";

const data = {
  audio_url: uploadUrl,
};

const response = await axios.post(base_url + "/v2/transcript", data, {
  headers,
});

const transcript_id = response.data.id;
const polling_endpoint = base_url + `/v2/transcript/${transcript_id}`;

while (true) {
  const transcript = (await axios.get(polling_endpoint, { headers })).data;

  if (transcript.status === "completed") {
    break;
  } else if (transcript.status === "error") {
    throw new Error(`Transcription failed: ${transcript.error}`);
  } else {
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}

// Step 2: Define your prompt.
const prompt = "What was the emotional sentiment of the phone call?";

// Step 3: Apply LeMUR.
const lemur_data = {
  prompt: prompt,
  transcript_ids: [transcript_id],
  final_model: "anthropic/claude-sonnet-4-20250514",
};

const result = await axios.post(
  base_url + "/lemur/v3/generate/task",
  lemur_data,
  { headers }
);
console.log(result.data.response);
