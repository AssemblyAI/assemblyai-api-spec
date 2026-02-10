using (var httpClient = new HttpClient())
{
    httpClient.DefaultRequestHeaders.Authorization =
        new AuthenticationHeaderValue("<YOUR_API_KEY>");
}
