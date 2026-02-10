data = {
  "audio_url" => upload_url,
  "sentiment_analysis" => true,
  "speaker_labels" => true
}
# ...
    transcription_result['sentiment_analysis_results'].each do |sentiment_result|
      puts sentiment_result['speaker']
    end
