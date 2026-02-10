const transcriber = client.streaming.transcriber({
  sampleRate: 16_000,
  formatTurns: true,
});
