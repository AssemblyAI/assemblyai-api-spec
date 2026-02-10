const params: TranscribeParams = {
  audio: audioUrl,
  redact_pii: true,
  redact_pii_policies: ["person_name", "organization", "occupation"],
  redact_pii_audio: true,
  redact_pii_audio_quality: "wav", // Optional. Defaults to "mp3"
};

const run = async () => {
  const transcript = await client.transcripts.transcribe(params);

  const { status, redacted_audio_url } = await client.transcripts.redactedAudio(
    transcript.id
  );

  console.log(`Status: ${status}, Redacted audio URL: ${redacted_audio_url}`);
};

run();
