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
            JArray contentSafetyLabels = (JArray)pollingResponseJson["content_safety_labels"];

            // Uncomment the next line to print everything
            // Console.WriteLine(contentSafetyLabels.ToString())

            foreach (JObject label in contentSafetyLabels) {
                // The severity score measures how severe the flagged content is on a scale of 0-1, with 1 being the most severe.
                if (label["name"].ToString() == "hate_speech" && (double)label["severity"] >= 0.5) {
                    Console.WriteLine($"Hate speech detected with severity score: {label["severity"]}");
                    // Do something with this information, such as flagging the transcription for review
                }
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
