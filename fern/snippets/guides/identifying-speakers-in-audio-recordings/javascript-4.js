const transcriptId = response.data.id;
const pollingEndpoint = `${baseUrl}/transcript/${transcriptId}`;

while (true) {
  const pollingResponse = await axios.get(pollingEndpoint, {
    headers: headers,
  });
  const transcriptionResult = pollingResponse.data;

  if (transcriptionResult.status === "completed") {
    const utterances = transcriptionResult.utterances;

    // Iterate through each utterance and print the speaker and the text they spoke
    for (const utterance of utterances) {
      const speaker = utterance.speaker;
      const text = utterance.text;
      console.log(`Speaker ${speaker}: ${text}`);
    }

    break;
  } else if (transcriptionResult.status === "error") {
    throw new Error(`Transcription failed: ${transcriptionResult.error}`);
  } else {
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}
