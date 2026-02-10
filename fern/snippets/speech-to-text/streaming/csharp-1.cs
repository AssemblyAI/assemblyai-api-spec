string[] list = { "aws", "azure", "google cloud" };
string wordBoost = Uri.EscapeDataString(JsonSerializer.Serialize(list));

string url = $"wss://api.assemblyai.com/v2/realtime/ws?sample_rate={SAMPLE_RATE}&word_boost={wordBoost}";
await ws.ConnectAsync(new Uri(url), cts.Token);
