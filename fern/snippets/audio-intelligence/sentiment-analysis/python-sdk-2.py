config = aai.TranscriptionConfig(
  sentiment_analysis=True,
  speaker_labels=True
)
# ...
for sentiment_result in transcript.sentiment_analysis:
  print(sentiment_result.speaker)
