$ch = curl_init("https://api.assemblyai.com/lemur/v3/generate/task");
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => $headers,
    CURLOPT_POSTFIELDS => json_encode([
        'final_model' => 'anthropic/claude-sonnet-4-20250514',
        'prompt' => $prompt,
        'transcript_ids' => [$transcript_id]
    ])
]);

$response = curl_exec($ch);
