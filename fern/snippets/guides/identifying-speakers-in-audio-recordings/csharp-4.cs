using (var client = new HttpClient())
{
    ...

    var responseJson = JsonConvert.DeserializeObject<dynamic>(responseContent);

    string transcriptId = responseJson.id;
    string pollingEndpoint = $"https://api.assemblyai.com/v2/transcript/{transcriptId}";

    while (true)
    {
        var pollingResponse = await client.GetAsync(pollingEndpoint);
        var pollingResponseContent = await pollingResponse.Content.ReadAsStringAsync();
        var pollingResponseJson = JsonConvert.DeserializeObject<dynamic>(pollingResponseContent);

        if (pollingResponseJson.status == "completed")
        {
            JArray utterances = (JArray)pollingResponseJson["utterances"];

            // Iterate through each utterance and print the speaker and the text they spoke
            foreach (JObject utterance in utterances) {
                string speaker = utterance["speaker"].ToString();
                string text = utterance["text"].ToString();
                Console.WriteLine($"Speaker {speaker}: {text}");
            }

            return pollingResponseJson;
        }
        else if (pollingResponseJson.status == "error")
        {
            throw new Exception($"Transcription failed: {pollingResponseJson.error}");
        }
        else
        {
            Thread.Sleep(3000);
        }
    }
}
