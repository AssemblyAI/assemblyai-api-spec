import { Readable } from "stream";
import { AssemblyAI } from "assemblyai";
import recorder from "node-record-lpcm16";

const run = async () => {
  const client = new AssemblyAI({
    apiKey: "<YOUR_API_KEY>",
  });

  const transcriber = client.streaming.transcriber({
    sampleRate: 16_000,
    formatTurns: true,
  });

  transcriber.on("open", ({ id }) => {
    console.log(`Session opened with ID: ${id}`);
  });

  transcriber.on("error", (error) => {
    console.error("Error:", error);
  });

  transcriber.on("close", (code, reason) =>
    console.log("Session closed:", code, reason)
  );

  transcriber.on("turn", (turn) => {
    if (!turn.transcript) {
      return;
    }

    console.log("Turn:", turn.transcript);
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
