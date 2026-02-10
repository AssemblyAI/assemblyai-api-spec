# Count the number of unique speaker labels
unique_speakers = set(utterance.speaker for utterance in transcript.utterances)

questions = []
for speaker in unique_speakers:
    questions.append(
        aai.LemurQuestion(
        question=f"Who is speaker {speaker}?",
        answer_format="<First Name> <Last Name (if applicable)>")

    )

result = aai.Lemur().question(
    questions,
    input_text=text_with_speaker_labels,
    final_model=aai.LemurModel.claude3_5_sonnet,
    context="Your task is to infer the speaker's name from the speaker-labelled transcript"
)
