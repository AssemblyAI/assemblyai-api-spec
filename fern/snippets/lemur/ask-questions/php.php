<?php
// Step 1: Transcribe an audio file.
$base_url = "https://api.assemblyai.com";
$headers = array(
    "authorization: <YOUR_API_KEY>",
    "content-type: application/json"
);

// $path = "/my_audio.mp3";
// $ch = curl_init($base_url . "/v2/upload");
// curl_setopt_array($ch, [
//     CURLOPT_POST => true,
//     CURLOPT_POSTFIELDS => file_get_contents($path),
//     CURLOPT_HTTPHEADER => $headers,
//     CURLOPT_RETURNTRANSFER => true
// ]);

// $response = curl_exec($ch);
// $upload_url = json_decode($response, true)["upload_url"];
// curl_close($ch);

// Or use a publicly-accessible URL:
$upload_url = "https://assembly.ai/sports_injuries.mp3";

$ch = curl_init($base_url . "/v2/transcript");
curl_setopt_array($ch, [
    CURLOPT_POST => true,
    CURLOPT_POSTFIELDS => json_encode(["audio_url" => $upload_url]), // You can also replace upload_url with an audio file URL
    CURLOPT_HTTPHEADER => $headers,
    CURLOPT_RETURNTRANSFER => true
]);

$response = curl_exec($ch);
$transcript_id = json_decode($response, true)['id'];
curl_close($ch);

$polling_endpoint = $base_url . "/v2/transcript/" . $transcript_id;

while (true) {
    $ch = curl_init($polling_endpoint);
    curl_setopt_array($ch, [
        CURLOPT_HTTPHEADER => $headers,
        CURLOPT_RETURNTRANSFER => true
    ]);

    $transcription_result = json_decode(curl_exec($ch), true);
    curl_close($ch);

    if ($transcription_result['status'] === "completed") {
        break;
    } else if ($transcription_result['status'] === "error") {
        throw new Exception("Transcription failed: " . $transcription_result['error']);
    }
    sleep(3);
}

// Step 2: Define a prompt with your question(s).
$prompt = "What is a runner's knee?";

// Step 3: Send to LLM Gateway.
$ch = curl_init("https://llm-gateway.assemblyai.com/v1/chat/completions");
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => $headers,
    CURLOPT_POSTFIELDS => json_encode([
        'model' => 'claude-sonnet-4-5-20250929',
        'messages' => [
            ['role' => 'user', 'content' => $prompt . "\n\nTranscript: " . $transcription_result['text']]
        ],
        'max_tokens' => 1000
    ])
]);

$response = curl_exec($ch);
$result = json_decode($response, true);
echo $result['choices'][0]['message']['content'];
curl_close($ch);
