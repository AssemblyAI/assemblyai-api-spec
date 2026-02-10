$transcript_id = $response['id'];
$polling_endpoint = "https://api.assemblyai.com/v2/transcript/" . $transcript_id;

while (true) {
    $polling_response = curl_init($polling_endpoint);

    curl_setopt($polling_response, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($polling_response, CURLOPT_RETURNTRANSFER, true);

    $transcription_result = json_decode(curl_exec($polling_response), true);

    if ($transcription_result['status'] === "completed") {
        // Print each auto chapter
        foreach ($transcription_result['auto_chapters'] as $chapter) {
            echo "Chapter Start Time: " . $chapter['start'] . "\n";
            echo "Chapter End Time: " . $chapter['end'] . "\n";
            echo "Chapter Headline: " . $chapter['headline'] . "\n";
            echo "Chapter Gist: " . $chapter['gist'] . "\n";
            echo "Chapter Summary: " . $chapter['summary'] . "\n";
        }
        break;
    } else if ($transcription_result['status'] === "error") {
        throw new Exception("Transcription failed: " . $transcription_result['error']);
    } else {
        sleep(3);
    }
}
