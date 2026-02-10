from deepgram import (
    DeepgramClient,
    PrerecordedOptions
)

API_KEY = "YOUR_DG_API_KEY"

AUDIO_URL = {
    "url": "https://dpgr.am/spacewalk.wav"
}

def main():
    try:
        deepgram = DeepgramClient(API_KEY)

        options = PrerecordedOptions(
            model="nova-2",
            smart_format=True,
            diarize=True
        )

        response = deepgram.listen.prerecorded.v("1").transcribe_url(AUDIO_URL, options)

        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")

if name == "main":
    main()
