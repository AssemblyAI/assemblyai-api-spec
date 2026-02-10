$data = array(
    "audio_url" => $upload_url,
    "sentiment_analysis" => true,
    "speaker_labels" => true
);
# ...
    foreach ($transcription_result['sentiment_analysis_results'] as $sentiment_result) {
        echo $sentiment_result['speaker'] . "\n";
    }
