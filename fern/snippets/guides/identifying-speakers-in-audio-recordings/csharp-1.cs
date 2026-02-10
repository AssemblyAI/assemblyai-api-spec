public async Task<string> UploadFileAsync(string apiKey, string path)
{
    using var client = new HttpClient();
    client.DefaultRequestHeaders.Authorization = new System.Net.Http.Headers.AuthenticationHeaderValue(apiKey);

    using var fileContent = new ByteArrayContent(File.ReadAllBytes(path));
    fileContent.Headers.ContentType = new System.Net.Http.Headers.MediaTypeHeaderValue("application/octet-stream");

    HttpResponseMessage response;
    try
    {
        response = await client.PostAsync("https://api.assemblyai.com/v2/upload", fileContent);
    }
    catch (Exception e)
    {
        Console.Error.WriteLine($"Error: {e.Message}");
        return null;
    }

    if (response.IsSuccessStatusCode)
    {
        string responseBody = await response.Content.ReadAsStringAsync();
        var json = JObject.Parse(responseBody);
        return json["upload_url"].ToString();
    }
    else
    {
        Console.Error.WriteLine($"Error: {response.StatusCode} - {response.ReasonPhrase}");
        return null;
    }
}
