# extract all utterances from the response
utterances = transcript.utterances

# For each utterance, print its speaker and what was said
for utterance in utterances:
  speaker = utterance.speaker
  text = utterance.text
  print(f"Speaker {speaker}: {text}")
