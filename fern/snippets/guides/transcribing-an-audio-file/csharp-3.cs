private static async Task<string> UploadFileAsync(string filePath, HttpClient httpClient)
{
    using (var fileStream = File.OpenRead(filePath))
    using (var fileContent = new StreamContent(fileStream))
    {
        fileContent.Headers.ContentType = new MediaTypeHeaderValue("application/octet-stream");

        using (var response = await httpClient.PostAsync("https://api.assemblyai.com/v2/upload", fileContent))
        {
            response.EnsureSuccessStatusCode();
            var jsonDoc = await response.Content.ReadFromJsonAsync<JsonDocument>();
            return jsonDoc.RootElement.GetProperty("upload_url").GetString();
        }
    }
}
