from pydub import AudioSegment

# Store utterances from each clip, keyed by clip index
clip_utterances = {}

# Dictionary to track known speaker identities across all clips
# Maps current clip speaker labels to a unified speaker label
speaker_identity_map = {}

def process_clips(clip_transcript_ids, audio_files):
    global clip_utterances, speaker_identity_map

    # This will store the longest clip filenames for each speaker from the previous clips
    previous_speaker_clips = {}

    for clip_index, (transcript_id, audio_file) in enumerate(zip(clip_transcript_ids, audio_files)):
        transcript = get_transcript(transcript_id)
        utterances = transcript['utterances']
        clip_utterances[clip_index] = utterances # Store utterances for the current clip

        longest_monologues = find_longest_monologues(utterances)

        # Process the longest monologues for clipping and storing
        current_speaker_clips = {}
        for speaker, monologue_data in longest_monologues.items():
            clip_and_store_utterances(audio_file, {speaker: monologue_data})
            longest_clip = f"{speaker}_monologue_{monologue_data[0][1]['start']}_{monologue_data[0][1]['end']}.wav"
            current_speaker_clips[speaker] = longest_clip

        if clip_index == 0:
            speaker_identity_map = {speaker: speaker for speaker in longest_monologues.keys()}
            previous_speaker_clips = current_speaker_clips.copy()
        else:
            # Compare all new speakers against all base speakers from previous clips
            for new_speaker, new_clip in current_speaker_clips.items():
                for base_speaker, base_clip in previous_speaker_clips.items():
                    if compare_embeddings(new_clip, base_clip):
                        speaker_identity_map[new_speaker] = base_speaker
                        break
                else:
                    # If no match is found, assign a new label
                    new_label = chr(ord(max(speaker_identity_map.values(), key=lambda x: ord(x))) + 1)
                    speaker_identity_map[new_speaker] = new_label

            # Update the previous_speaker_clips for the next iteration
            previous_speaker_clips.update(current_speaker_clips)

        # Update utterances with the new speaker labels for the current clip
        for utterance in clip_utterances[clip_index]:
            original_speaker = utterance['speaker']
            # Update only if there's a change in speaker identity
            if original_speaker in speaker_identity_map:
                utterance['speaker'] = speaker_identity_map[original_speaker]


# Add your clip transcript IDs
clip_transcript_ids = [
    "YOUR_TRANSCRIPT_ID_1",
    "YOUR_TRANSCRIPT_ID_2",
    "YOUR_TRANSCRIPT_ID_3"
]

# Add filepaths to your downloaded files
audio_files = [
    "/testone.wav",
    "/testtwo.wav",
    "/testthree.wav"
]

process_clips(clip_transcript_ids, audio_files)
