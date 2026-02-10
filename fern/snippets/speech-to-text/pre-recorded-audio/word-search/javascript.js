import axios from "axios";
import fs from "fs-extra";

const baseUrl = "https://api.assemblyai.com";

const headers = {
  authorization: "<YOUR_API_KEY>",
};

const path = "./my-audio.mp3";
const audioData = await fs.readFile(path);
const uploadResponse = await axios.post(`${baseUrl}/v2/upload`, audioData, {
  headers,
});
const uploadUrl = uploadResponse.data.upload_url;

const data = {
  audio_url: uploadUrl, // You can also use a URL to an audio or video file on the web
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
};

const url = `${baseUrl}/v2/transcript`;
const transcript = await axios.post(url, data, { headers: headers });

const transcriptId = transcript.data.id;
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

const words = ["foo", "bar", "foo bar", "42"];

const response = await axios.get(
  `${baseUrl}/v2/transcript/${transcriptId}/word-search?words=${words.join(",")}`,
  { headers }
);

for (const match of response.data.matches) {
  console.log(`Found '${match.text}' ${match.count} times in the transcript`);
}
