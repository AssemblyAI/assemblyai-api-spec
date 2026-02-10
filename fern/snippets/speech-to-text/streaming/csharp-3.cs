await ws.SendAsync(
    new ArraySegment<byte>(Encoding.UTF8.GetBytes("{\"force_end_utterance\": true}")),
    WebSocketMessageType.Text,
    true,
    CancellationToken.None
);
