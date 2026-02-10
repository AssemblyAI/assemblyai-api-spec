import assemblyai as aai
import requests
import json
import time
import requests
import copy
from pydub import AudioSegment
import os
import nemo.collections.asr as nemo_asr
from pydub import AudioSegment

speaker_model = nemo_asr.models.EncDecSpeakerLabelModel.from_pretrained("nvidia/speakerverification_en_titanet_large")

assemblyai_key = "YOUR_API_KEY"

headers = {
    "authorization": assemblyai_key
}

def get_transcript(transcript_id):
    polling_endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"

    while True:
        transcription_result = requests.get(polling_endpoint, headers=headers).json()

        if transcription_result['status'] == 'completed':
            # print("Transcript ID:", transcript_id)
            return(transcription_result)
            break

        elif transcription_result['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

        else:
            time.sleep(3)

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

file_one = "YOUR_FILE_1"
file_two = "YOUR_FILE_2"
file_three = "YOUR_FILE_3"

download_wav(file_one, "testone.wav")
download_wav(file_two, "testtwo.wav")
download_wav(file_three, "testthree.wav")

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

def display_transcript(transcript_data):
    for clip_index, utterances in transcript_data.items():
        print(f"Clip {clip_index + 1}:")
        for utterance in utterances:
            speaker = utterance['speaker']
            text = utterance['text']
            print(f"  Speaker {speaker}: {text}")
        print("\n")  # Add an extra newline for spacing between


display_transcript(clip_utterances)
