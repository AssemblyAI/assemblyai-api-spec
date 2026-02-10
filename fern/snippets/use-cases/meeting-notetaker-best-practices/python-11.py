# First, transcribe with speaker diarization
transcript = transcriber.transcribe(audio_url, config=aai.TranscriptionConfig(speaker_labels=True))

# Later, add speaker identification
transcript_dict = transcript.json_response

# Add speaker identification
transcript_dict["speech_understanding"] = {
    "request": {
        "speaker_identification": {
            "speaker_type": "name",
            "known_values": ["Sarah Chen", "Michael Rodriguez"]
        }
    }
}

# Send to Speech Understanding API
import requests
result = requests.post(
    "https://llm-gateway.assemblyai.com/v1/understanding",
    headers={"Authorization": aai.settings.api_key},
    json=transcript_dict
).json()

# Access identified speakers
for utterance in result["utterances"]:
    print(f"{utterance['speaker']}: {utterance['text']}")
