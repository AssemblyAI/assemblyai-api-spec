import axios from "axios";
import fs from "fs-extra";

const baseUrl = "https://api.assemblyai.com";

const headers = {
  authorization: "<YOUR_API_KEY>",
};

const transcriptId = "<TRANSCRIPT_ID>";
const pollingEndpoint = `${baseUrl}/v2/transcript/${transcriptId}`;

const pollingResponse = await axios.get(pollingEndpoint, {
  headers: headers,
});
const transcriptionResult = pollingResponse.data;

if (transcriptionResult.status === "completed") {
  console.log(transcriptionResult.text);
} else if (transcriptionResult.status === "error") {
  throw new Error(`Transcription failed: ${transcriptionResult.error}`);
}
