import axios from "axios";
import fs from "fs-extra";

const baseUrl = "https://api.assemblyai.com";

const headers = {
  authorization: "YOUR_API_KEY",
};

async function transcribe() {
  // Use a publicly-accessible URL
  const audioFile = "https://assembly.ai/wildfires.mp3";

  // Or upload a local file:
  // const audioData = await fs.readFile("./example.mp3");
  // const uploadResponse = await axios.post(`${baseUrl}/v2/upload`, audioData, { headers });
  // const audioFile = uploadResponse.data.upload_url;

  const data = {
    audio_url: audioFile,
    speech_models: ["universal-3-pro", "universal-2"],
    language_detection: true,
    speaker_labels: true,
  };

  const transcriptResponse = await axios.post(
    `${baseUrl}/v2/transcript`,
    data,
    { headers }
  );
  const transcriptId = transcriptResponse.data.id;
  const pollingEndpoint = `${baseUrl}/v2/transcript/${transcriptId}`;

  while (true) {
    const pollingResponse = await axios.get(pollingEndpoint, { headers });
    const transcript = pollingResponse.data;

    if (transcript.status === "completed") {
      console.log(`\nFull Transcript:\n\n${transcript.text}`);

      // Optionally print speaker diarization results
      // for (const utterance of transcript.utterances) {
      //   console.log(`Speaker ${utterance.speaker}: ${utterance.text}`);
      // }
      break;
    } else if (transcript.status === "error") {
      throw new Error(`Transcription failed: ${transcript.error}`);
    } else {
      await new Promise((resolve) => setTimeout(resolve, 3000));
    }
  }
}

transcribe();
