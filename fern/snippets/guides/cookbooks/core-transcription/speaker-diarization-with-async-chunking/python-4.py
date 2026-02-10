def download_wav(presigned_url, output_filename):
    # Download the WAV file from the presigned URL
    response = requests.get(presigned_url)
    if response.status_code == 200:
        print("downloading...")
        with open(output_filename, 'wb') as f:
            f.write(response.content)
        print("successfully downloaded file:", output_filename)
    else:
        raise Exception("Failed to download file, status code: {}".format(response.status_code))

# Function to identify the longest monologue of each speaker from each clip
# you pass in the utterances and it returns the longest monologue from each speaker on that file
def find_longest_monologues(utterances):
    longest_monologues = {}
    current_monologue = {}
    last_speaker = None  # Track the last speaker to identify interruptions

    for utterance in utterances:
        speaker = utterance['speaker']
        start_time = utterance['start']
        end_time = utterance['end']

        if speaker not in current_monologue:
            current_monologue[speaker] = {"start": start_time, "end": end_time}
            longest_monologues[speaker] = []
        else:
            # Extend monologue only if it's the same speaker speaking continuously
            if current_monologue[speaker]["end"] == start_time and last_speaker == speaker:
                current_monologue[speaker]["end"] = end_time
            else:
                monologue_length = current_monologue[speaker]["end"] - current_monologue[speaker]["start"]
                new_entry = (monologue_length, copy.deepcopy(current_monologue[speaker]))

                if len(longest_monologues[speaker]) < 1 or monologue_length > min(longest_monologues[speaker], key=lambda x: x[0])[0]:
                    if len(longest_monologues[speaker]) == 1:
                        longest_monologues[speaker].remove(min(longest_monologues[speaker], key=lambda x: x[0]))

                    longest_monologues[speaker].append(new_entry)

                current_monologue[speaker] = {"start": start_time, "end": end_time}

        last_speaker = speaker  # Update the last speaker

    # Check the last monologue for each speaker
    for speaker, monologue in current_monologue.items():
        monologue_length = monologue["end"] - monologue["start"]
        new_entry = (monologue_length, monologue)
        if len(longest_monologues[speaker]) < 1 or monologue_length > min(longest_monologues[speaker], key=lambda x: x[0])[0]:
            if len(longest_monologues[speaker]) == 1:
                longest_monologues[speaker].remove(min(longest_monologues[speaker], key=lambda x: x[0]))
            longest_monologues[speaker].append(new_entry)

    return longest_monologues

# Create clips of each long monologue and embed the clip
# you pass in the file path and the longest monologue objects returned by the find_longest_monologues function.
# This function will create new audio file clips which contain only the longest monologue from each speaker
def clip_and_store_utterances(audio_file, longest_monologues):
    # Load the full conversation audio
    full_audio = AudioSegment.from_wav(audio_file)
    full_audio = full_audio.set_channels(1)

    utterance_clips = []

    for speaker, monologues in longest_monologues.items():
        for _, monologue in monologues:
            start_ms = monologue['start']
            end_ms = monologue['end']
            clip = full_audio[start_ms:end_ms]
            clip_filename = f"{speaker}_monologue_{start_ms}_{end_ms}.wav"
            clip.export(clip_filename, format="wav")

            utterance_clips.append({
                'clip_filename': clip_filename,
                'start': start_ms,
                'end': end_ms,
                'speaker': speaker
            })

    print("Total Number of Monologue Clips Found: ", len(utterance_clips))

    return utterance_clips

# This function uses NeMO to compare two files
def compare_embeddings(utterance_clip, reference_file):
    verification_result = speaker_model.verify_speakers(
        utterance_clip,
        reference_file
    )
    return verification_result
