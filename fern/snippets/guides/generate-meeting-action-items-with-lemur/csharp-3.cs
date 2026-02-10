string transcriptId = response.Content.ReadAsAsync<dynamic>().Result.id;
string pollingEndpoint = $"https://api.assemblyai.com/v2/transcript/{transcriptId}";

while (true) {
    var pollingRequest = new HttpRequestMessage {
        Method = HttpMethod.Get,
        RequestUri = new Uri(pollingEndpoint),
        Headers = {
            { "authorization", "<YOUR_API_KEY>" }
        }
    };

    var pollingResponse = httpClient.SendAsync(pollingRequest).Result;
    var transcriptionResult = JObject.Parse(pollingResponse.Content.ReadAsStringAsync().Result);

    if (transcriptionResult["status"].ToString() == "completed") {
        break;
    } else if (transcriptionResult["status"].ToString() == "error") {
        throw new Exception($"Transcription failed: {transcriptionResult["error"]}");
    } else {
        Thread.Sleep(3000);
    }
}
