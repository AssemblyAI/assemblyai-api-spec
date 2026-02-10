const data = {
  audio_url: uploadUrl, // You can also use a URL to an audio or video file on the web
  redact_pii: true,
  redact_pii_policies: ["person_name", "organization", "occupation"],
  redact_pii_sub: "hash",
  redact_pii_audio: true,
  redact_pii_audio_quality: "wav", // Optional. Defaults to "mp3"
};

// ...
const redactedAudioPollingEndpoint = `${baseUrl}/v2/transcript/${transcriptId}/redacted-audio`;

while (true) {
  const redactedAudioPollingResponse = await axios.get(
    redactedAudioPollingEndpoint,
    {
      headers: headers,
    }
  );
  const redactedAudioResult = redactedAudioPollingResponse.data;

  if (redactedAudioResult.status === "redacted_audio_ready") {
    console.log(redactedAudioResult.redacted_audio_url);
    break;
  } else if (redactedAudioResult.status === "error") {
    throw new Error(`Transcription failed: ${redactedAudioResult.error}`);
  } else {
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}
