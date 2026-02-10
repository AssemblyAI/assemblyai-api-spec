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
