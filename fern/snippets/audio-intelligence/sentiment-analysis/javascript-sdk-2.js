const params = {
  audio: audioUrl,
  sentiment_analysis: true,
  speaker_labels: true,
};
// ...
for (const result of transcript.sentiment_analysis_results) {
  console.log(result.speaker);
}
