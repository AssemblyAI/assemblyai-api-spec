private static async Task<Transcript> CreateTranscriptAsync(string audioUrl, HttpClient httpClient)
{
    var data = new { audio_url = audioUrl };
    var content = new StringContent(JsonSerializer.Serialize(data), Encoding.UTF8, "application/json");

    using (var response = await httpClient.PostAsync("https://api.assemblyai.com/v2/transcript", content))
    {
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<Transcript>();
    }
}
