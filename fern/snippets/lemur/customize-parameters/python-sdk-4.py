text_with_speaker_labels = ""
for utt in transcript.utterances:
    text_with_speaker_labels += f"Speaker {utt.speaker}:\n{utt.text}\n"

result = aai.Lemur().task(
    prompt,
    final_model,
    input_text=text_with_speaker_labels
)
