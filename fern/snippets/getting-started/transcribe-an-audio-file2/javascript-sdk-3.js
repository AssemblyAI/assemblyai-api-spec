if (transcript.status === "error") {
  throw new Error(`Transcription failed: ${transcript.error}`);
}

console.log(`\nFull Transcript:\n\n${transcript.text}`);
