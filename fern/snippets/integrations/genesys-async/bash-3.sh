{
  version: '2',
  id: '<id>',
  type: 'close',
  seq: 5,
  position: 'PT10.2S',
  parameters: { reason: 'end' },
  serverseq: 4
}
Handling close message
Closing file stream
Converting raw audio to WAV: '<wav file name>'

# Skipping ffmpeg output for brevity...

Uploading recording '<raw file>' to S3
Successfully uploaded raw recording to S3: '<raw file>'
Successfully uploaded WAV recording to S3: '<wav file>'
Sent closed response, seq=5
WebSocket closed for session '<session_id>': code=1000, reason=Session Ended
Cleaning up session '<session_id>'
Deleted local raw recording file: '<raw_file>'
Deleted local WAV recording file: '<wav_file>'
