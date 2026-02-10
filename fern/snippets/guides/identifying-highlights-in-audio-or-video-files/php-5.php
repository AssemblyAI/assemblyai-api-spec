$transcript_id = $response['id'];
$polling_endpoint = "https://api.assemblyai.com/v2/transcript/" . $transcript_id;

while (true) {
    $polling_response = curl_init($polling_endpoint);

    curl_setopt($polling_response, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($polling_response, CURLOPT_RETURNTRANSFER, true);

    $transcription_result = json_decode(curl_exec($polling_response), true);

    if ($transcription_result['status'] === "completed") {
        $auto_highlights_result = $transcription_result['auto_highlights_result'];
        foreach ($auto_highlights_result['results'] as $highlight) {
            echo "Highlight: " . $highlight['text'] . ", Count: " . $highlight['count'] . ", Rank: " . $highlight['rank'] . ", Timestamps: " . implode(",", $highlight['timestamps']) . "\n";
        }
        break;
    } else if ($transcription_result['status'] === "error") {
        throw new Exception("Transcription failed: " . $transcription_result['error']);
    } else {
        sleep(3);
    }
}
