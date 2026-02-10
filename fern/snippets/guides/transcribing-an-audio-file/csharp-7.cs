using (var httpClient = new HttpClient())
{
    httpClient.DefaultRequestHeaders.Authorization =
        new AuthenticationHeaderValue("<YOUR_API_KEY>");

    var uploadUrl = await UploadFileAsync("/my_audio.mp3", httpClient);
    var transcript = await CreateTranscriptAsync(uploadUrl, httpClient);
    transcript = await WaitForTranscriptToProcess(transcript, httpClient);

    Console.WriteLine(transcript.Text);
}
