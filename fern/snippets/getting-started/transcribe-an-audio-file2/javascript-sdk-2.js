const params = {
  audio: audioFile,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  speaker_labels: true,
};

const transcript = await client.transcripts.transcribe(params);
