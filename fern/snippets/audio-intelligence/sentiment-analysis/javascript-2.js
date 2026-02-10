const data = {
  audio_url: uploadUrl,
  sentiment_analysis: true,
  speaker_labels: true
}
// ...
    for sentimentResult of transcriptionResult['sentiment_analysis_results']:
      console.log(sentimentResult['speaker'])
    break
