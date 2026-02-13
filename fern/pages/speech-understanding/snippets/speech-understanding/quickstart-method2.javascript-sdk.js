const { AssemblyAI } = require("assemblyai");

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

// Need to transcribe a local file? Learn more here: https://www.assemblyai.com/docs/getting-started/transcribe-an-audio-file
const audioUrl = "https://assembly.ai/wildfires.mp3";

async function transcribeAndIdentifySpeakers() {
  const transcript = await client.transcripts.transcribe({
    audio_url: audioUrl,
    speaker_labels: true,
  });

  // Enable speaker identification
  const result = await client.speechUnderstanding.understand({
    transcript_id: transcript.id,
    speech_understanding: {
      request: {
        speaker_identification: {
          speaker_type: "name",
          known_values: ["Michel Martin", "Peter DeCarlo"], // Change these values to match the names of the speakers in your file
        },
      },
    },
  });

  // Access the results and print utterances to the terminal
  for (const utterance of result.utterances) {
    console.log(`${utterance.speaker}: ${utterance.text}`);
  }
}

transcribeAndIdentifySpeakers();
