from deepgram import (
     DeepgramClient,
     PrerecordedOptions,
     FileSource,
)

API_KEY = "YOUR_DG_API_KEY"

AUDIO_FILE = "./example.wav"

def main():
    try:
        deepgram = DeepgramClient(API_KEY)

        with open(AUDIO_FILE, "rb") as file:
            buffer_data = file.read()

            payload: FileSource = {
                "buffer": buffer_data,
            }

            options = PrerecordedOptions(
                model="nova-2",
                smart_format=True,
                diarize=True
            )

            response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)

            print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")

if name == "main":
    main()
