import requests
import time
import json
import pyaudio
import websocket
import threading
from urllib.parse import urlencode
from datetime import datetime
import os
from pathlib import Path


YOUR_API_KEY = "<YOUR_API_KEY>"  # Replace with your API key
AUDIO_FOLDER_PATH = "<YOUR_AUDIO_FILE_FOLDER>"  # Folder containing audio files

# Audio Configuration
SAMPLE_RATE = 16000
CHANNELS = 1
FORMAT = pyaudio.paInt16
FRAMES_PER_BUFFER = 800  # 50ms of audio (0.05s * 16000Hz)

# Global variables for audio stream and websocket
audio = None
stream = None
ws_app = None
audio_thread = None
stop_event = threading.Event()
recorded_frames = []
recording_lock = threading.Lock()

# Store the optimized configuration
OPTIMIZED_CONFIG = {}
