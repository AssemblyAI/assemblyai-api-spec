import assemblyai as aai

aai.settings.api_key = "<YOUR_API_KEY>"

audio_url = "https://assembly.ai/meeting.mp4"
transcript = aai.Transcriber().transcribe(audio_url)

result = transcript.lemur.summarize(
    final_model=aai.LemurModel.claude_sonnet_4_20250514,
    context="A GitLab meeting to discuss logistics",
    answer_format="TLDR"
)

print(result.response)
