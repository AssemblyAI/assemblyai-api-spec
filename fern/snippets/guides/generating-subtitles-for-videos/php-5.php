function getSubtitleFile(string $transcriptId, string $fileFormat): string {
    if (!in_array($fileFormat, ['srt', 'vtt'])) {
        throw new Exception("Unsupported file format: {$fileFormat}. Please specify 'srt' or 'vtt'.");
    }

    $url = "https://api.assemblyai.com/v2/transcript/{$transcriptId}/{$fileFormat}";

    $curl = curl_init();
    curl_setopt_array($curl, [
        CURLOPT_URL => $url,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER => $headers,
    ]);

    $response = curl_exec($curl);
    $httpCode = curl_getinfo($curl, CURLINFO_HTTP_CODE);

    if ($httpCode === 200) {
        return $response;
    } else {
        throw new Exception("Failed to retrieve {$fileFormat} file: {$httpCode} " . curl_error($curl));
    }
}

$subtitlesText = getSubtitleFile(transcriptId, "vtt"); // or "srt"
echo $subtitlesText
