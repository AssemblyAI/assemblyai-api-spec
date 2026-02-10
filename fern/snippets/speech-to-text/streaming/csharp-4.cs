await ws.SendAsync(
    new ArraySegment<byte>(Encoding.UTF8.GetBytes("{\"end_utterance_silence_threshold\": 300}")),
    WebSocketMessageType.Text,
    true,
    CancellationToken.None
);
