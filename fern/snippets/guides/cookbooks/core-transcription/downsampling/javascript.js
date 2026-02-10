import { spawn } from "child_process";

function convertAudio(inputFile, outputFile) {
  return new Promise((resolve, reject) => {
    const ffmpeg = spawn("ffmpeg", [
      "-i",
      inputFile,
      "-ar",
      "16000",
      "-ac",
      "1",
      "-ab",
      "128k",
      outputFile,
    ]);

    ffmpeg.on("close", (code) => {
      if (code === 0) {
        console.log("Conversion successful!");
        resolve();
      } else {
        reject(new Error(`FFmpeg exited with code ${code}`));
      }
    });

    ffmpeg.stderr.on("data", (data) => {
      console.error(`Error: ${data}`);
    });
  });
}

// Usage
convertAudio("input.wav", "output.mp3")
  .then(() => console.log("Done!"))
  .catch((err) => console.error(err));
