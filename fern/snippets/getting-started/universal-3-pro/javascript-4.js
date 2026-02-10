import axios from "axios";

const baseUrl = "https://api.assemblyai.com";
const headers = {
  authorization: "<YOUR_API_KEY>",
};

const data = {
  audio_url: "https://assemblyaiassets.com/audios/ouput_formatting.mp3",
  language_detection: true,
  speech_models: ["universal-3-pro", "universal-2"],
  prompt:
    "Add punctuation based on the speaker's tone and expressiveness. Use exclamation marks (!) when the speaker is yelling, excited, or emphatic. Use question marks (?) for questioning intonation. Apply standard punctuation (periods, commas) based on natural speech patterns and pauses.",
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
