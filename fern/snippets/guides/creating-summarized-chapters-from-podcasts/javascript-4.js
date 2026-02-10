const transcriptId = response.data.id;
const pollingEndpoint = `${baseUrl}/transcript/${transcriptId}`;

while (true) {
  const pollingResponse = await axios.get(pollingEndpoint, {
    headers: headers,
  });
  const transcriptionResult = pollingResponse.data;

  if (transcriptionResult.status === "completed") {
    // Print each auto chapter
    transcriptionResult.chapters.forEach((chapter: any) => {
      console.log("Chapter Start Time:", chapter.start);
      console.log("Chapter End Time:", chapter.end);
      console.log("Chapter Headline:", chapter.headline);
      console.log("Chapter Gist:", chapter.gist);
      console.log("Chapter Summary:", chapter.summary);
    });
    break;
  } else if (transcriptionResult.status === "error") {
    throw new Error(`Transcription failed: ${transcriptionResult.error}`);
  } else {
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}
