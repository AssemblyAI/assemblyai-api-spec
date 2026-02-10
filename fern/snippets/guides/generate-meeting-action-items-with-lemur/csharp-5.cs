var data = new Dictionary<string, dynamic>(){
    { "transcript_ids", new string [] {transcriptId} },
    { "prompt", prompt }
};

using (var client = new HttpClient())
{
    client.DefaultRequestHeaders.Add("authorization", apiKey);
    var content = new StringContent(JsonConvert.SerializeObject(data), Encoding.UTF8, "application/json");
    HttpResponseMessage response = await client.PostAsync("https://api.assemblyai.com/lemur/v3/generate/task", content);
    var responseContent = await response.Content.ReadAsStringAsync();
    var result = JsonConvert.DeserializeObject<dynamic>(responseContent);

    Console.WriteLine(response.Content.ReadAsAsync<dynamic>().Result.response);
}
