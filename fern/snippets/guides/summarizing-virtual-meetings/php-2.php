$path = "/my_audio.mp3";

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, $base_url . "/upload");
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, file_get_contents($path));
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);

$response = curl_exec($ch);
$response_data = json_decode($response, true);
$upload_url = $response_data["upload_url"];

curl_close($ch);
