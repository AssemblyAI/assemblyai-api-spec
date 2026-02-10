import axios from "axios";
import fs from "fs-extra";

const baseUrl = "https://api.assemblyai.com";

const headers = {
  authorization: "<YOUR_API_KEY>",
};

const path = "./my-audio.mp3";
const audioData = await fs.readFile(path);
const uploadResponse = await axios.post(`${baseUrl}/v2/upload`, audioData, {
  headers,
});
const uploadUrl = uploadResponse.data.upload_url;

const data = {
  audio_url: uploadUrl, // You can also use a URL to an audio or video file on the web
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  content_safety: true,
};

const url = `${baseUrl}/v2/transcript`;
const response = await axios.post(url, data, { headers: headers });

const transcriptId = response.data.id;
console.log("Transcript ID: ", transcriptId);

const pollingEndpoint = `${baseUrl}/v2/transcript/${transcriptId}`;

while (true) {
  const pollingResponse = await axios.get(pollingEndpoint, {
    headers: headers,
  });
  const transcriptionResult = pollingResponse.data;

  if (transcriptionResult.status === "completed") {
    const contentSafetyLabels = transcriptionResult.content_safety_labels;
    for (const result of contentSafetyLabels.results) {
      console.log(result.text);
      console.log(
        `Timestamp: ${result.timestamp.start} - ${result.timestamp.end}`
      );

      // Get category, confidence, and severity.
      for (const label of result.labels) {
        console.log(`${label.label} - ${label.confidence} - ${label.severity}`); // content safety category
      }
    }
    // Get the confidence of the most common labels in relation to the entire audio file
    for (const [label, confidence] of Object.entries(
      contentSafetyLabels.summary
    )) {
      console.log(
        `${confidence * 100}% confident that the audio contains ${label}`
      );
    }
    // Get the confidence of the most common labels in relation to the entire audio file.
    for (const [label, severity_confidence] of Object.entries(
      contentSafetyLabels.severity_score_summary
    )) {
      console.log(
        `${severity_confidence.low * 100}% confident that the audio contains low-severity ${label}`
      );
      console.log(
        `${severity_confidence.medium * 100}% confident that the audio contains medium-severity ${label}`
      );
      console.log(
        `${severity_confidence.high * 100}% confident that the audio contains high-severity ${label}`
      );
    }

    break;
  } else if (transcriptionResult.status === "error") {
    throw new Error(`Transcription failed: ${transcriptionResult.error}`);
  } else {
    await new Promise((resolve) => setTimeout(resolve, 3000));
  }
}
