import { AssemblyAI } from "assemblyai";

const client = new AssemblyAI({
  apiKey: "<YOUR_API_KEY>",
});

// const audioFile = './local_file.mp3'
const audioFile = "https://assembly.ai/wildfires.mp3";

const params = {
  audio: audioFile,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  content_safety: true,
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);
  console.log(`Transcript ID: ${transcript.id}`);
  const contentSafetyLabels = transcript.content_safety_labels;

  // Get the parts of the transcript which were flagged as sensitive
  for (const result of contentSafetyLabels.results) {
    console.log(result.text);
    console.log(
      `Timestamp: ${result.timestamp.start} - ${result.timestamp.end}`
    );

    // Get category, confidence, and severity
    for (const label of result.labels) {
      console.log(`${label.label} - ${label.confidence} - ${label.severity}`);
    }
  }

  // Get the confidence of the most common labels in relation to the entire audio file
  for (const [label, confidence] of Object.entries(
    contentSafetyLabels.summary
  )) {
    console.log(
      `${confidence * 100}% confident that the audio contains ${label}`
    );
  }

  // Get the overall severity of the most common labels in relation to the entire audio file
  for (const [label, severity_confidence] of Object.entries(
    contentSafetyLabels.severity_score_summary
  )) {
    console.log(
      `${severity_confidence.low * 100}% confident that the audio contains low-severity ${label}`
    );
    console.log(
      `${severity_confidence.medium * 100}% confident that the audio contains medium-severity ${label}`
    );
    console.log(
      `${severity_confidence.high * 100}% confident that the audio contains high-severity ${label}`
    );
  }
};
run();
