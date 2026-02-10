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

const srtEndpoint = `${baseUrl}/v2/transcript/${transcriptId}/srt?chars_per_caption=32`;
const srtResponse = await axios.get(srtEndpoint, { headers });
const srt = srtResponse.data;

fs.writeFileSync(`transcript_${transcriptId}.srt`, srt);

// const vttEndpoint = `${baseUrl}/v2/transcript/${transcriptId}/vtt?chars_per_caption=32`
// const vttResponse = await axios.get(vttEndpoint, { headers })
// const vtt = vttResponse.data

// fs.writeFileSync(`transcript_${transcriptId}.vtt`, vtt)
