const list = ["aws", "azure", "google cloud"];
const wordBoost = encodeURIComponent(JSON.stringify(list));
const ws = new WebSocket(
    `wss://api.assemblyai.com/v2/realtime/ws?sample_rate=${SAMPLE_RATE}&word_boost=${wordBoost}`,
    ...,
  );
