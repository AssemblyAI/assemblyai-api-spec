# Get participant names from Zoom meeting
zoom_participants = get_zoom_meeting_participants(meeting_id)
speaker_names = [p["name"] for p in zoom_participants]

# Use in speaker identification
config = aai.TranscriptionConfig(
    speaker_labels=True,
    speakers_expected=len(speaker_names),  # Hint: exact number of speakers
    speech_understanding={
        "request": {
            "speaker_identification": {
                "speaker_type": "name",
                "known_values": speaker_names
            }
        }
    }
)
