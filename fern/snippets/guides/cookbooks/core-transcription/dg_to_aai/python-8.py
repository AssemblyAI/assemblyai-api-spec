options = PrerecordedOptions(
   model="nova-2",
   smart_format=True,
   diarize=True,
   detect_entities=True
)

response = deepgram.listen.prerecorded.v("1").transcribe_url(AUDIO_URL, options)
