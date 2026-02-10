let textWithSpeakerLabels = "";
for (const utt of transcript.utterances) {
  textWithSpeakerLabels += `Speaker ${utt.speaker}:\n${utt.text}\n`;
}

const { response } = await client.lemur.task({
  prompt: prompt,
  final_model: final_model,
  input_text: textWithSpeakerLabels,
});
