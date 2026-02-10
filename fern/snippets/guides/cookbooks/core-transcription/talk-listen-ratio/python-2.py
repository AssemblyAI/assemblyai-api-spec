def calculate_talk_listen_ratios(transcript):
    """
    :param transcript: AssemblyAI Transcript object
    :return: Dictionary with talk time, percentage, and talk-listen ratios for each speaker
    """
    # Ensure speaker labels were enabled
    if not transcript.utterances:
        raise ValueError("Speaker labels were not enabled for this transcript.")

    speaker_talk_time = {}
    total_time = 0

    for utterance in transcript.utterances:
        speaker = f"Speaker {utterance.speaker}"
        duration = utterance.end - utterance.start

        speaker_talk_time[speaker] = speaker_talk_time.get(speaker, 0) + duration
        total_time += duration

    # Calculate percentages and ratios
    result = {}
    for speaker, talk_time in speaker_talk_time.items():
        percentage = (talk_time / total_time) * 100
        result[speaker] = {
            "talk_time_ms": talk_time,
            "percentage": round(percentage, 2)
        }

    # Calculate talk-listen ratios for each speaker against all others
    for speaker in result.keys():
        other_speakers_time = sum(talk_time for spk, talk_time in speaker_talk_time.items() if spk != speaker)
        if other_speakers_time > 0:
            ratio = speaker_talk_time[speaker] / other_speakers_time
            result[speaker]["talk_listen_ratio"] = round(ratio, 2)
        else:
            result[speaker]["talk_listen_ratio"] = None  # Handle cases with only one speaker

    return result
