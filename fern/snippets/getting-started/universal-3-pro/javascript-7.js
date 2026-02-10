import axios from "axios";

const baseUrl = "https://api.assemblyai.com";
const headers = {
  authorization: "<YOUR_API_KEY>",
};

const data = {
  audio_url: "https://assemblyaiassets.com/audios/speaker_diarization.mp3",
  language_detection: true,
  speech_models: ["universal-3-pro", "universal-2"],
  speaker_labels: true,
  prompt:
    "Produce a transcript with every disfluency data. Additionally, label speakers with their respective roles. 1. Place [Speaker:role] at the start of each speaker turn. Example format: [Speaker:NURSE] Hello there. How can I help you today? [Speaker:PATIENT] I'm feeling unwell. I have a headache.",
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
