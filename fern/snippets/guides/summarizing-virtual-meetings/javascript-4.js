const transcriptId = response.data.id;
const pollingEndpoint = `${baseUrl}/transcript/${transcriptId}`;

while (true) {
  const pollingResponse = await axios.get(pollingEndpoint, {
    headers: headers,
  });
  const transcriptionResult = pollingResponse.data;

  if (transcriptionResult.status === "completed") {
    const summary = transcriptionResult.summary || "";
    console.log("Transcription completed!");
    console.log(`Transcription: ${transcriptionResult.text}`);
    console.log(`Summary: ${summary}`);
    break;
  } else if (transcriptionResult.status === "error") {
    throw new Error(`Transcription failed: ${transcriptionResult.error}`);
  } else {
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}
