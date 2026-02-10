def identify_speakers_from_utterances(transcript, wav_file, min_utterance_length=5000, match_all_utterances=False):
    utterances = transcript["utterances"]
    speaker_model = EncDecSpeakerLabelModel.from_pretrained("nvidia/speakerverification_en_titanet_large")

    known_speakers = {}
    unknown_speakers = {}
    unknown_count = 0

    unknown_folder = "unknown_speaker_utterances"
    os.makedirs(unknown_folder, exist_ok=True)

    audio_file_name = os.path.basename(wav_file)
    full_audio = AudioSegment.from_wav(wav_file)

    def get_suitable_utterance(speaker, min_length):
        suitable_utterances = [
            u for u in utterances if u["speaker"] == speaker and (u["end"] - u["start"]) >= min_length
        ]
        if suitable_utterances:
            return max(suitable_utterances, key=lambda u: u["end"] - u["start"])
        return max((u for u in utterances if u["speaker"] == speaker), key=lambda u: u["end"] - u["start"])

    # First pass: Identify speakers.
    for speaker in set(u["speaker"] for u in utterances):
        if speaker not in known_speakers and speaker not in unknown_speakers:
            suitable_utterance = get_suitable_utterance(speaker, min_utterance_length)

            start_ms = suitable_utterance["start"]
            end_ms = suitable_utterance["end"]
            utterance_audio = full_audio[start_ms:end_ms]

            temp_wav = "temp_utterance.wav"
            utterance_audio.export(temp_wav, format="wav")
            embedding = speaker_model.get_embedding(temp_wav)
            os.remove(temp_wav)

            speaker_name, score = find_closest_speaker(embedding)
            print(f"Speaker: {speaker}, Closest match: {speaker_name}, Score: {score}")

            if score > 0.5:  # Adjust threshold as needed.
                known_speakers[speaker] = speaker_name
                print(f"Identified as known speaker: {speaker}")
            else:
                unknown_count += 1
                unknown_name = f"Unknown Speaker {chr(64 + unknown_count)}"
                unknown_wav = f"{unknown_folder}/unknown_speaker_{unknown_count}_from_{audio_file_name}"
                utterance_audio.export(unknown_wav, format="wav")
                unknown_speakers[speaker] = {
                    "name": unknown_name,
                    "wav_file": unknown_wav,
                    "duration": end_ms - start_ms,
                }
                print(f"New unknown speaker detected: {unknown_name} (Duration: {(end_ms - start_ms)/1000:.2f}s)")

    # Second pass: Replace speaker names.
    for utterance in utterances:
        if utterance["speaker"] in known_speakers:
            utterance["speaker"] in known_speakers[utterance["speaker"]]
        elif utterance["speaker"] in unknown_speakers:
            utterance["speaker"] = unknown_speakers[utterance["speaker"]]["name"]

    # Third pass: Match all utterances if requested.
    if match_all_utterances:
        print("Matching all utterances individually...")
        for utterance in utterances:
            start_ms = utterance["start"]
            end_ms = utterance["end"]
            utterance_audio = full_audio[start_ms:end_ms]

            temp_wav = "temp_utterance.wav"
            utterance_audio.export(temp_wav, format="wav")
            embedding = speaker_model.get_embedding(temp_wav)
            os.remove(temp_wav)

            new_speaker_name, score = find_closest_speaker(embedding)

            if score > 0.5 and new_speaker_name != utterance["speaker"]:
                print(f"Speaker change detected: '{utterance['speaker']}' -> '{new_speaker_name}' (Score: {score})")
                print(f"Utterance: {utterance['text'][:50]}...")
                utterance["speaker"] = new_speaker_name

    return utterances, unknown_speakers
