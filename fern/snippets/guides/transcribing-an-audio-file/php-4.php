$transcript_id = $response['id'];
echo "Transcript ID: $transcript_id\n";

$polling_endpoint = "https://api.assemblyai.com/v2/transcript/" . $transcript_id;

while (true) {
    $polling_response = curl_init($polling_endpoint);

    curl_setopt($polling_response, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($polling_response, CURLOPT_RETURNTRANSFER, true);

    $transcription_result = json_decode(curl_exec($polling_response), true);

    if ($transcription_result['status'] === "completed") {
        echo $transcription_result['text'];
        break;
    } else if ($transcription_result['status'] === "error") {
        throw new Exception("Transcription failed: " . $transcription_result['error']);
    } else {
        sleep(3);
    }
}
