private static async Task<Transcript> WaitForTranscriptToProcess(Transcript transcript, HttpClient httpClient)
{
    var pollingEndpoint = $"https://api.assemblyai.com/v2/transcript/{transcript.Id}";

    while (true)
    {
        var pollingResponse = await httpClient.GetAsync(pollingEndpoint);
        transcript = await pollingResponse.Content.ReadFromJsonAsync<Transcript>();
        switch (transcript.Status)
        {
            case "processing":
            case "queued":
                await Task.Delay(TimeSpan.FromSeconds(3));
                break;
            case "completed":
                return transcript;
            case "error":
                throw new Exception($"Transcription failed: {transcript.Error}");
            default:
                throw new Exception("This code shouldn't be reachable.");
        }
    }

}
