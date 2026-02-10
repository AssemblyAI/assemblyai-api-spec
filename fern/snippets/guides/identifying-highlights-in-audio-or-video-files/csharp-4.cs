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
        var autoHighlightsResult = transcriptionResult["auto_highlights_result"];
        foreach (var highlight in autoHighlightsResult["results"]) {
            Console.WriteLine($"Highlight: {highlight["text"]}, Count: {highlight["count"]}, Rank: {highlight["rank"]}, Timestamps: {string.Join(",", highlight["timestamps"])}");
        }
        break;
    } else if (transcriptionResult["status"].ToString() == "error") {
        throw new Exception($"Transcription failed: {transcriptionResult["error"]}");
    } else {
        Thread.Sleep(3000);
    }
}
