import { Readable } from "stream";
import { AssemblyAI } from "assemblyai";
import recorder from "node-record-lpcm16";

const run = async () => {
  const client = new AssemblyAI({
    apiKey: "<YOUR_API_KEY>",
  });

  const transcriber = client.streaming.transcriber({
    sampleRate: 16_000,
    speechModel: "whisper-streaming",
    languageDetection: true,
  });

  transcriber.on("open", ({ id }) => {
    console.log(`Connecting websocket to url`);
    console.log(`Session opened with ID: ${id}`);
    console.log(`Receiving SessionBegins ...`);
    console.log(`Sending messages ...`);
  });

  transcriber.on("error", (error) => {
    console.error("Error:", error);
  });

  transcriber.on("close", (code, reason) =>
    console.log("Session closed:", code, reason)
  );

  transcriber.on("turn", (turn) => {
    if (!turn.end_of_turn && turn.transcript) {
      console.log(`[PARTIAL TURN TRANSCRIPT]: ${turn.transcript}`);
    }
    if (turn.utterance) {
      console.log(`[PARTIAL TURN UTTERANCE]: ${turn.utterance}`);
      // Display language detection info if available
      if (turn.language_code) {
        const langConfidence = (turn.language_confidence * 100).toFixed(2);
        console.log(
          `[UTTERANCE LANGUAGE DETECTION]: ${turn.language_code} - ${langConfidence}%`
        );
      }
    }
    if (turn.end_of_turn) {
      console.log(`[FULL TURN TRANSCRIPT]: ${turn.transcript}`);
      // Display language detection info if available
      if (turn.language_code) {
        const langConfidence = (turn.language_confidence * 100).toFixed(2);
        console.log(
          `[END OF TURN LANGUAGE DETECTION]: ${turn.language_code} - ${langConfidence}%`
        );
      }
    }
  });

  try {
    console.log("Connecting to streaming transcript service");

    await transcriber.connect();

    console.log("Starting recording");

    const recording = recorder.record({
      channels: 1,
      sampleRate: 16_000,
      audioType: "wav", // Linear PCM
    });

    Readable.toWeb(recording.stream()).pipeTo(transcriber.stream());

    // Stop recording and close connection using Ctrl-C.

    process.on("SIGINT", async function () {
      console.log();
      console.log("Stopping recording");
      recording.stop();

      console.log("Closing streaming transcript connection");
      await transcriber.close();

      process.exit();
    });
  } catch (error) {
    console.error(error);
  }
};

run();
