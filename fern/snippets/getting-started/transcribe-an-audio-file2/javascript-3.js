const data = {
  audio_url: audioFile,
  speech_models: ["universal-3-pro", "universal-2"],
  language_detection: true,
  speaker_labels: true,
};

const transcriptResponse = await axios.post(`${baseUrl}/v2/transcript`, data, {
  headers,
});
const transcriptId = transcriptResponse.data.id;
