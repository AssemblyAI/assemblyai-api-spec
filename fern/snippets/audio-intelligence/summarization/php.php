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
    "summarization" => true,
    "summary_model" => "informative",
    "summary_type" => "bullets"
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
        echo $transcription_result['summary'];
        break;
    } else if ($transcription_result['status'] === "error") {
        throw new Exception("Transcription failed: " . $transcription_result['error']);
    } else {
        sleep(3);
    }
}
