YOUR_API_KEY = "YOUR_API_KEY"  # Replace with your AssemblyAI API key
AUDIO_FILE = "audio.wav"  # Path to your audio file
SAMPLE_RATE = 48000  # Change to match the sample rate of your audio file
SAVE_TRANSCRIPT_TO_FILE = True  # Set to False to disable saving transcript to file
PLAY_AUDIO = True  # Set to False to disable audio playback

# Track session data for output file
session_data = {
    "session_id": None,
    "parameters": None,
    "audio_file": AUDIO_FILE,
    "audio_duration_seconds": None,
    "turns": []
}
