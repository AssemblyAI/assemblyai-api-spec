var data = new Dictionary<string, dynamic>(){
    { "audio_url", upload_url }
};

using (var client = new HttpClient())
{
    client.DefaultRequestHeaders.Add("authorization", apiKey);
    var content = new StringContent(JsonConvert.SerializeObject(data), Encoding.UTF8, "application/json");
    HttpResponseMessage response = await client.PostAsync("https://api.assemblyai.com/v2/transcript", content);
    var responseContent = await response.Content.ReadAsStringAsync();
    var responseJson = JsonConvert.DeserializeObject<dynamic>(responseContent);
}
