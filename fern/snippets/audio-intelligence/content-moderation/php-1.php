<?php
$ch = curl_init();
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$base_url = "https://api.assemblyai.com";

$headers = array(
    "authorization: <YOUR_API_KEY>",
    "content-type: application/json"
);

$path = "./local_file.mp3";

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, $base_url . "/v2/upload");
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, file_get_contents($path));
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

$response = curl_exec($ch);
$response_data = json_decode($response, true);
$upload_url = $response_data["upload_url"];

curl_close($ch);

$data = array(
    "audio_url" => $upload_url, // You can also use a URL to an audio or video file on the web
    "speech_models" => array("universal-3-pro", "universal-2"),
    "language_detection" => true,
    "content_safety" => true,
);

$url = $base_url . "/v2/transcript";
$curl = curl_init($url);

curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($curl);

$response = json_decode($response, true);

curl_close($curl);

$transcript_id = $response['id'];
echo "Transcript ID: $transcript_id\n";

$polling_endpoint = $base_url . "/v2/transcript/" . $transcript_id;

while (true) {
    $polling_response = curl_init($polling_endpoint);

    curl_setopt($polling_response, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($polling_response, CURLOPT_RETURNTRANSFER, true);

    $transcription_result = json_decode(curl_exec($polling_response), true);

    if ($transcription_result['status'] === "completed") {
        $content_safety_labels = $transcription_result['content_safety_labels'];

        foreach ($content_safety_labels['results'] as $result) {
          echo $result['text'] . "\n";
          echo "Timestamp: {$result['timestamp']['start']} - {$result['timestamp']['end']}\n";

          // Get category, confidence, and severity.
          foreach ($result['labels'] as $label) {
            echo "{$label['label']} - {$label['confidence']} - {$label['severity']}\n"; // content safety category
          }
        }
        // Get the confidence of the most common labels in relation to the entire audio file.
        foreach ($transcription_result['content_safety_labels']['summary'] as $label => $confidence) {
          echo round($confidence * 100, 2) . "% confident that the audio contains $label\n";
        }
        // Get the confidence of the most common labels in relation to the entire audio file.
        foreach ($content_safety_labels['severity_score_summary'] as $label => $severity_confidence) {
          echo ($severity_confidence['low'] * 100) . "% confident that the audio contains low-severity {$label}\n";
          echo ($severity_confidence['medium'] * 100) . "% confident that the audio contains medium-severity {$label}\n";
          echo ($severity_confidence['high'] * 100) . "% confident that the audio contains high-severity {$label}\n";
        }
        break;
    }  else if ($transcription_result['status'] === "error") {
        throw new Exception("Transcription failed: " . $transcription_result['error']);
    } else {
        sleep(3);
    }
}
