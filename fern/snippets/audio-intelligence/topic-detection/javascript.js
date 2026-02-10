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
  iab_categories: true,
};

const url = `${baseUrl}/v2/transcript`;
const response = await axios.post(url, data, { headers: headers });

const transcriptId = response.data.id;
console.log("Transcript ID: ", transcriptId);

const pollingEndpoint = `${baseUrl}/v2/transcript/${transcriptId}`;

while (true) {
  const pollingResponse = await axios.get(pollingEndpoint, {
    headers: headers,
  });
  const transcriptionResult = pollingResponse.data;

  if (transcriptionResult.status === "completed") {
    // Get the parts of the transcript that were tagged with topics
    for (const result of transcriptionResult.iab_categories_result.results) {
      console.log(result.text);
      console.log(
        `Timestamp: ${result.timestamp.start} - ${result.timestamp.end}`
      );

      for (const label of result.labels) {
        console.log(`${label.label} (${label.relevance})`);
      }
    }
    // Get a summary of all topics in the transcript
    for (const [topic, relevance] of Object.entries(
      transcriptionResult.iab_categories_result.summary
    )) {
      console.log(`Audio is ${relevance * 100} relevant to ${topic}`);
    }
  } else if (transcriptionResult.status === "error") {
    throw new Error(`Transcription failed: ${transcriptionResult.error}`);
  } else {
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}
