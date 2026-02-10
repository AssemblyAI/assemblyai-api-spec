const pollingEndpoint = `${baseUrl}/v2/transcript/${transcriptId}`;

while (true) {
  const pollingResponse = await axios.get(pollingEndpoint, { headers });
  const transcript = pollingResponse.data;

  if (transcript.status === "completed") {
    console.log(`\nFull Transcript:\n\n${transcript.text}`);
    break;
  } else if (transcript.status === "error") {
    throw new Error(`Transcription failed: ${transcript.error}`);
  } else {
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}
