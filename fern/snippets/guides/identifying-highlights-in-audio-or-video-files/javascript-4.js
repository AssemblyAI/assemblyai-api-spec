const transcriptId = response.data.id;
const pollingEndpoint = `${baseUrl}/transcript/${transcriptId}`;

while (true) {
  const pollingResponse = await axios.get(pollingEndpoint, {
    headers: headers,
  });
  const transcriptionResult = pollingResponse.data;

  if (transcriptionResult.status === "completed") {
    const autoHighlightsResult = transcriptionResult.auto_highlights_result;
    for (const highlight of autoHighlightsResult.results) {
      const timestamps = highlight.timestamps
        .map((timestamp) => `${timestamp.start}ms-${timestamp.end}ms`)
        .join(", ");
      console.log(
        `Highlight: ${highlight.text}, Count: ${highlight.count}, Rank: ${highlight.rank}, Timestamps: ${timestamps}`
      );
    }
    break;
  } else if (transcriptionResult.status === "error") {
    throw new Error(`Transcription failed: ${transcriptionResult.error}`);
  } else {
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}
