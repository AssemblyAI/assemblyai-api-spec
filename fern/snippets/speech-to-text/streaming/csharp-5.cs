// Define a callback to handle the session information message
if (messageType == "SessionInformation" && root.TryGetProperty("audio_duration_seconds", out JsonElement audioDurationSecondsElement))
{
    double audioDurationSeconds = audioDurationSecondsElement.GetDouble();
    Console.WriteLine($"Audio duration: {audioDurationSeconds}");
    return;
}

// Configure the on_extra_session_information parameter
string url = $"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={SAMPLE_RATE}&on_extra_session_information=true";
await ws.ConnectAsync(new Uri(url), cts.Token);
