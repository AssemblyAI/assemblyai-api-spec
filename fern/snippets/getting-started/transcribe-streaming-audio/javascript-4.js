// Audio Configuration
const SAMPLE_RATE = CONNECTION_PARAMS.sample_rate;
const CHANNELS = 1;
// Global variables
let micInstance = null;
let micInputStream = null;
let ws = null;
let stopRequested = false;
// WAV recording variables
let recordedFrames = []; // Store audio frames for WAV file
// --- Helper functions ---
function clearLine() {
  process.stdout.write("\r" + " ".repeat(80) + "\r");
}
function formatTimestamp(timestamp) {
  return new Date(timestamp * 1000).toISOString();
}
function createWavHeader(sampleRate, channels, dataLength) {
  const buffer = Buffer.alloc(44);

  // RIFF header
  buffer.write("RIFF", 0);
  buffer.writeUInt32LE(36 + dataLength, 4);
  buffer.write("WAVE", 8);

  // fmt chunk
  buffer.write("fmt ", 12);
  buffer.writeUInt32LE(16, 16); // fmt chunk size
  buffer.writeUInt16LE(1, 20); // PCM format
  buffer.writeUInt16LE(channels, 22);
  buffer.writeUInt32LE(sampleRate, 24);
  buffer.writeUInt32LE(sampleRate * channels * 2, 28); // byte rate
  buffer.writeUInt16LE(channels * 2, 32); // block align
  buffer.writeUInt16LE(16, 34); // bits per sample

  // data chunk
  buffer.write("data", 36);
  buffer.writeUInt32LE(dataLength, 40);

  return buffer;
}
function saveWavFile() {
  if (recordedFrames.length === 0) {
    console.log("No audio data recorded.");
    return;
  }

  // Generate filename with timestamp
  const timestamp = new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19);
  const filename = `recorded_audio_${timestamp}.wav`;

  try {
    // Combine all recorded frames
    const audioData = Buffer.concat(recordedFrames);
    const dataLength = audioData.length;

    // Create WAV header
    const wavHeader = createWavHeader(SAMPLE_RATE, CHANNELS, dataLength);

    // Write WAV file
    const wavFile = Buffer.concat([wavHeader, audioData]);
    fs.writeFileSync(filename, wavFile);

    console.log(`Audio saved to: ${filename}`);
    console.log(
      `Duration: ${(dataLength / (SAMPLE_RATE * CHANNELS * 2)).toFixed(2)} seconds`
    );
  } catch (error) {
    console.error(`Error saving WAV file: ${error}`);
  }
}
