import axios from "axios";

const baseUrl = "https://api.assemblyai.com";
const headers = {
  authorization: "<YOUR_API_KEY>",
};

const data = {
  audio_url: "https://assemblyaiassets.com/audios/verbatim.mp3",
  language_detection: true,
  speech_models: ["universal-3-pro", "universal-2"],
  prompt:
    "Produce a transcript suitable for conversational analysis. Every disfluency is meaningful data. Include: fillers (um, uh, er, ah, hmm, mhm, like, you know, I mean), repetitions (I I, the the), restarts (I was- I went), stutters (th-that, b-but, no-not), and informal speech (gonna, wanna, gotta)",
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
