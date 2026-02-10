$data = array(
    "transcript_ids" => [$transcript_id],
    "prompt" => $prompt
);

$url = "https://api.assemblyai.com/lemur/v3/generate/task";
$curl = curl_init($url);

curl_setopt($curl, CURLOPT_POST, true);
curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($data));
curl_setopt($curl, CURLOPT_HTTPHEADER, $headers);
curl_setopt($curl, CURL_RETURNTRANSFER, true);

$result = json_decode(curl_exec($curl), true);
curl_close($curl);

echo $result["response"];
