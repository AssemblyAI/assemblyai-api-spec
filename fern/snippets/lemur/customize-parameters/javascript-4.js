let textWithSpeakerLabels = "";
for (const utt of transcript.utterances) {
  textWithSpeakerLabels += `Speaker ${utt.speaker}:\n${utt.text}\n`;
}

const data = {
  prompt: prompt,
  final_model: final_model,
  input_text: textWithSpeakerLabels,
};

const result = await axios.post(
  "https://api.assemblyai.com/lemur/v3/generate/task",
  data,
  { headers }
);
