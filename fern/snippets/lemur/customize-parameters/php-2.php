$ch = curl_init("https://api.assemblyai.com/lemur/v3/generate/task");
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => $headers,
    CURLOPT_POSTFIELDS => json_encode([
        'transcript_ids' => [$transcript_id]
        'prompt' => $prompt,
        'final_model' => $final_model,
        'max_output_size' => 1000
    ])
]);

$response = curl_exec($ch);
