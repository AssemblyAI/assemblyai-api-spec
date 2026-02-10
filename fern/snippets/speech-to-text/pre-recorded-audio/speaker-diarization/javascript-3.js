import axios from "axios";
import fs from "fs-extra";

const baseUrl = "https://api.assemblyai.com";

const headers = {
  authorization: "<YOUR_API_KEY>",
};

const path = "./audio/audio.mp3";
const audioData = await fs.readFile(path);

const uploadResponse = await axios.post(`${baseUrl}/v2/upload`, audioData, {
  headers,
});

const uploadUrl = uploadResponse.data.upload_url;

const data = {
  audio_url: uploadUrl, // You can also use a URL to an audio or video file on the web
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  speaker_labels: true,
  speaker_options: {
    min_speakers_expected: 3,
    max_speakers_expected: 5,
  },
};

const url = `${baseUrl}/v2/transcript`;
const response = await axios.post(url, data, { headers });

const transcriptId = response.data.id;
const pollingEndpoint = `${baseUrl}/v2/transcript/${transcriptId}`;

while (true) {
  const pollingResponse = await axios.get(pollingEndpoint, { headers });
  const transcriptionResult = pollingResponse.data;

  if (transcriptionResult.status === "completed") {
    for (const utterance of transcriptionResult.utterances) {
      console.log(`Speaker ${utterance.speaker}: ${utterance.text}`);
    }
    break;
  } else if (transcriptionResult.status === "error") {
    throw new Error(`Transcription failed: ${transcriptionResult.error}`);
  } else {
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}
