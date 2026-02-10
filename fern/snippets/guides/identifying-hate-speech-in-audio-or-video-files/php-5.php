$transcript_id = $response['id'];
$polling_endpoint = "https://api.assemblyai.com/v2/transcript/" . $transcript_id;

while (true) {
    $polling_response = curl_init($polling_endpoint);

    curl_setopt($polling_response, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($polling_response, CURLOPT_RETURNTRANSFER, true);

    $transcription_result = json_decode(curl_exec($polling_response), true);

    if ($transcription_result['status'] === "completed") {
        $content_safety_labels = $transcription_result['content_safety_labels'];

        // Uncomment the next line to print everything
        // echo $content_safety_labels

        foreach ($content_safety_labels as $label) {
            // The severity score measures how severe the flagged content is on a scale of 0-1, with 1 being the most severe.
            if ($label['name'] === 'hate_speech' && $label['severity'] >= 0.5) {
                echo "Hate speech detected with severity score: " . $label['severity'] . "\n";
                // Do something with this information, such as flagging the transcription for review
            }
        }
        break;
    } else if ($transcription_result['status'] === "error") {
        throw new Exception("Transcription failed: " . $transcription_result['error']);
    } else {
        sleep(3);
    }
}
