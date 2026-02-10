import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

# Step 1: Transcribe an audio file.
# audio_file = "./local_file.mp4"
# Or use a publicly-accessible URL:
audio_file = "https://assembly.ai/call.mp4"

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(audio_file)

# Step 2: Define your prompt.
prompt = "What was the emotional sentiment of the phone call?"

# Step 3: Apply LeMUR.
result = transcript.lemur.task(
    prompt, final_model=aai.LemurModel.claude_sonnet_4_20250514
)

print(result.response)
