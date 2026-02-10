data = {
    "audio_url": upload_url,
    "sentiment_analysis": True,
    "speaker_labels": True
}
# ...
      for sentiment_result in transcription_result['sentiment_analysis_results']:
        print(sentiment_result['speaker'])
      break
