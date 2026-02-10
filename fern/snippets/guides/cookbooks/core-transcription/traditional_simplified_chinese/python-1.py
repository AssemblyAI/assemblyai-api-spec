import assemblyai as aai
import opencc

aai.settings.api_key = "<YOUR-API-KEY>"

audio_file = "https://assembly.ai/chinese-interview.mp4"

config = aai.TranscriptionConfig(language_code="zh")

transcript = aai.Transcriber(config=config).transcribe(audio_file)

if transcript.status == "error":
  raise RuntimeError(f"Transcription failed: {transcript.error}")

# t2s.json converts traditional characters to simplified
# use s2t.json to convert from simplified to traditional
converter = opencc.OpenCC('t2s.json')

simplified_transcript = converter.convert(transcript.text)

print(simplified_transcript)
