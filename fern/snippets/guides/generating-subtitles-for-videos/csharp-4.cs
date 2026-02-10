public async Task<string> ExportSubtitlesAsync(string transcriptId, string format)
{
    // The URL of the AssemblyAI API endpoint for exporting subtitles
    string url = $"https://api.assemblyai.com/v2/transcript/{transcriptId}/{format}";

    // Create a new HttpClient to make the HTTP requests
    using (var client = new HttpClient())
    {
        // Set the "authorization" header with your API key
        client.DefaultRequestHeaders.Add("authorization", apiKey);

        // Send a GET request to the API endpoint
        HttpResponseMessage response = await client.GetAsync(url);

        // Read the response content as a string
        var responseContent = await response.Content.ReadAsStringAsync();

        // Return the subtitles content as a string
        return responseContent;
    }
}
