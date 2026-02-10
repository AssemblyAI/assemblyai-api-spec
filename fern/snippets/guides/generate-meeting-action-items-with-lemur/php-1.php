$ch = curl_init();
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$base_url = "https://api.assemblyai.com/v2";

$headers = array(
  "authorization: <YOUR_API_KEY>",
  "content-type: application/json"
);
