// First get the request_id from a previous LeMUR task response
$request_id = $result['request_id'];

$delete_url = "https://api.assemblyai.com/lemur/v3/{$request_id}";
$ch = curl_init($delete_url);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_CUSTOMREQUEST => "DELETE",
    CURLOPT_HTTPHEADER => $headers
]);

$deletion_response = curl_exec($ch);
curl_close($ch);
