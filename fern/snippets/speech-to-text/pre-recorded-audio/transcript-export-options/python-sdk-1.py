import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# audio_file = "./local_file.mp3"
audio_file = "https://assembly.ai/wildfires.mp3"

config = aai.TranscriptionConfig(
  speech_models=["universal-3-pro", "universal-2"],
  language_detection=True
)

transcript = aai.Transcriber(config=config).transcribe(audio_file)

if transcript.status == "error":
  raise RuntimeError(f"Transcription failed: {transcript.error}")

srt = transcript.export_subtitles_srt(
  # Optional: Customize the maximum number of characters per caption
  chars_per_caption=32
  )

with open(f"transcript_{transcript.id}.srt", "w") as srt_file:
  srt_file.write(srt)

# vtt = transcript.export_subtitles_vtt()

# with open(f"transcript_{transcript_id}.vtt", "w") as vtt_file:
#   vtt_file.write(vtt)
