import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

// Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
const audioUrl = "https://assembly.ai/wildfires.mp3";

// Configure transcript with speaker identification
const config = {
  audio_url: audioUrl,
  speaker_labels: true,
  speech_understanding: {
    speaker_identification: {
      speaker_type: "name",
      known_values: ["Michel Martin", "Peter DeCarlo"], // Change these values to match the names of the speakers in your file
    },
  },
};

const transcript = await client.transcripts.transcribe(config);

// Access the results and print utterances to the console
for (const utterance of transcript.utterances) {
  console.log(`${utterance.speaker}: ${utterance.text}`);
}
