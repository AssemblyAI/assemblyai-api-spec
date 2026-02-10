$data = array(
    "audio_url" => $upload_url, // You can also use a URL to an audio or video file on the web
    "redact_pii" => true,
    "redact_pii_policies" => ["person_name", "organization", "occupation"],
    "redact_pii_sub" => "hash",
    "redact_pii_audio" => true,
    "redact_pii_audio_quality" => "wav" // Optional. Defaults to "mp3"
);

# ...
$redacted_audio_polling_endpoint = $base_url . "/v2/transcript/" . $transcript_id . "/redacted-audio";

while (true) {
    $redacted_audio_polling_response = curl_init($redacted_audio_polling_endpoint);

    curl_setopt($redacted_audio_polling_response, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($redacted_audio_polling_response, CURLOPT_RETURNTRANSFER, true);

    $redacted_audio_result = json_decode(curl_exec($redacted_audio_polling_response), true);

    if ($redacted_audio_result['status'] === "redacted_audio_ready") {
        echo $redacted_audio_result['redacted_audio_url'] . "\n";
        break;
    }  else if ($redacted_audio_result['status'] === "error") {
        throw new Exception("Transcription failed: " . $redacted_audio_result['error']);
    } else {
        sleep(3);
    }
}
