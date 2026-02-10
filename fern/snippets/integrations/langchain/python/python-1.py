audio_file = "https://assembly.ai/sports_injuries.mp3"
# or a local file path: audio_file = "./sports_injuries.mp3"

loader = AssemblyAIAudioTranscriptLoader(file_path=audio_file)

docs = loader.load()
