# Local Files
AUDIO_FILE = "example.wav"
with open(AUDIO_FILE, "rb") as file:
    buffer_data = file.read()

payload: FileSource = {
    "buffer": buffer_data,
}

options = PrerecordedOptions(
    smart_format=True,
    summarize="v2",
)

file_response = deepgram.listen.rest.v("1").transcribe_file(payload, options)

json = file_response.to_json()

#Public URLs
AUDIO_URL = {
    "url": "https://static.deepgram.com/examples/Bueller-Life-moves-pretty-fast.wav"
}

options = PrerecordedOptions(
    smart_format=True,
    summarize="v2"
)

url_response = deepgram.listen.rest.v("1").transcribe_url(AUDIO_URL, options)

json = url_response.to_json()
