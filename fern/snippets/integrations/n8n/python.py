transcript = _('Get a transcription').first().json
formatted_text = ''

if 'utterances' in transcript and transcript['utterances']:
    # Format with speaker labels
    for utterance in transcript['utterances']:
        formatted_text += f"Speaker {utterance['speaker']}: {utterance['text']}\n\n"
else:
    # Use plain text if no speaker labels
    formatted_text = transcript['text']

return {'formattedText': formatted_text}
