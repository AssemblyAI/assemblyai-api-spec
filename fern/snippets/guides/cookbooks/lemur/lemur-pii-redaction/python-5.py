transcript_text = transcription_result['text']
sentences = re.split(r'[.!?]+', transcript_text)
redacted_transcript = ''

for sentence in sentences:
    sentence = sentence.strip()
    if not sentence:
        continue

    generated_entities = generate_ner(sentence)
    redacted_sentence = sentence

    for entity in generated_entities:
        redacted_sentence = redacted_sentence.replace(entity, '#' * len(entity))

    redacted_transcript += redacted_sentence + '. '
    print(redacted_sentence)
