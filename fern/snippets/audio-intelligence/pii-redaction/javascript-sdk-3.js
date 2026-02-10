import fs from "fs/promises";

...

const audioFile = await client.transcripts.redactedAudioFile(transcript.id);
await fs.writeFile('./redacted-audio.wav', audioFile.body, 'binary');
