// Replace or establish new set of keyterms
websocket.send(
  '{"type": "UpdateConfiguration", "keyterms_prompt": ["Universal-3"]}'
);

// Remove keyterms and reset context biasing
websocket.send('{"type": "UpdateConfiguration", "keyterms_prompt": []}');
