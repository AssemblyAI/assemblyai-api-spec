<?php

$base_url = "https://api.assemblyai.com";

$headers = array(
    "authorization: <YOUR_API_KEY>",
    "content-type: application/json"
);

$path = "./audio.mp3";
if (!file_exists($path)) {
    throw new Exception("Audio file not found at $path");
}

// Upload the audio file
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "$base_url/v2/upload");
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, file_get_contents($path));
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

$response = curl_exec($ch);
if (curl_errno($ch)) {
    throw new Exception("Upload cURL error: " . curl_error($ch));
}

$response_data = json_decode($response, true);
if (!isset($response_data['upload_url'])) {
    throw new Exception("Upload failed: " . $response);
}
$upload_url = $response_data["upload_url"];
curl_close($ch);

// Start transcription
$data = array(
    "audio_url" => $upload_url,
    "speech_models" => array("universal-3-pro", "universal-2"),
    "language_detection" => true
);
$ch = curl_init("$base_url/v2/transcript");
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
if (curl_errno($ch)) {
    throw new Exception("Transcription start cURL error: " . curl_error($ch));
}

$response_data = json_decode($response, true);
if (!isset($response_data['id'])) {
    throw new Exception("Failed to create transcription: " . $response);
}

$transcript_id = $response_data['id'];
echo "Transcript ID: $transcript_id\n";
curl_close($ch);

// Poll for completion
$polling_endpoint = "$base_url/v2/transcript/$transcript_id";
while (true) {
    $ch = curl_init($polling_endpoint);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $polling_response = curl_exec($ch);
    if (curl_errno($ch)) {
        throw new Exception("Polling cURL error: " . curl_error($ch));
    }

    $transcription_result = json_decode($polling_response, true);
    curl_close($ch);

    if ($transcription_result['status'] === "completed") {
        echo "Transcription complete:\n" . $transcription_result['text'] . "\n";
        break;
    } elseif ($transcription_result['status'] === "error") {
        throw new Exception("Transcription failed: " . $transcription_result['error']);
    } else {
        sleep(3); // Wait and poll again
    }
}

// Optional: Word search
$words = ['foo', 'bar', 'foo bar', '42'];
$encoded_words = array_map('urlencode', $words);
$word_query = implode(',', $encoded_words);

$ch = curl_init("$base_url/v2/transcript/$transcript_id/word-search?words=$word_query");
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
if (curl_errno($ch)) {
    throw new Exception("Word search cURL error: " . curl_error($ch));
}

$response_data = json_decode($response, true);
curl_close($ch);

if (!isset($response_data['matches'])) {
    echo "No matches found or error in word search response:\n" . json_encode($response_data) . "\n";
} else {
    foreach ($response_data['matches'] as $match) {
        echo "Found '" . $match['text'] . "' " . $match['count'] . " times in the transcript\n";
    }
}
