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
  audio_url: uploadUrl,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  webhook_url: "https://example.com/webhook",
};

const url = `${baseUrl}/v2/transcript`;
const response = await axios.post(url, data, { headers: headers });
