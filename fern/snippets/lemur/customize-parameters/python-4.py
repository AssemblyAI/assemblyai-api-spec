text_with_speaker_labels = ""
for utt in transcript["utterances"]:
  text_with_speaker_labels += f"Speaker {utt["speaker"]}:\n{utt["text"]}\n"

data = {
  "prompt": prompt,
  "final_model": final_model,
  "input_text": text_with_speaker_labels
}

result = requests.post("https://api.assemblyai.com/lemur/v3/generate/task", headers=headers, json=data)
