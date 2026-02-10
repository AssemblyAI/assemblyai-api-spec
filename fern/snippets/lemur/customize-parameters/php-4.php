$text_with_speaker_labels = "";
foreach ($transcript['utterances'] as $utt) {
  $text_with_speaker_labels .= "Speaker {$utt['speaker']}:\n{$utt['text']}\n";
}

$ch = curl_init("https://api.assemblyai.com/lemur/v3/generate/task");
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => $headers,
    CURLOPT_POSTFIELDS => json_encode([
        'prompt' => $prompt,
        'final_model' => $final_model,
        'input_text' => $text_with_speaker_labels
    ])
]);

$response = curl_exec($ch);
