const transcriptId = response.data.id;
const pollingEndpoint = `${baseUrl}/transcript/${transcriptId}`;

while (true) {
  const pollingResponse = await axios.get(pollingEndpoint, {
    headers: headers,
  });
  const transcriptionResult = pollingResponse.data;

  if (transcriptionResult.status === "completed") {
    // Uncomment the next line to print everything
    // console.log(transcriptionResult.content_safety_labels)

    const contentSafetyLabels =
      transcriptionResult.content_safety_labels.results;
    contentSafetyLabels.forEach((label) => {
      const labels = label.labels;
      labels.forEach((label) => {
        // The severity score measures how severe the flagged content is on a scale of 0-1, with 1 being the most severe.
        if (label.label === "hate_speech" && label.severity >= 0.5) {
          console.log(
            `Hate speech detected with severity score: ${label.severity}`
          );
          // Do something with this information, such as flagging the transcription for review
        }
      });
    });
    break;
  } else if (transcriptionResult.status === "error") {
    throw new Error(`Transcription failed: ${transcriptionResult.error}`);
  } else {
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}
