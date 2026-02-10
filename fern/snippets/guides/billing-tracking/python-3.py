import websocket
import json
from urllib.parse import urlencode
from datetime import datetime

# Configuration
YOUR_API_KEY = "<YOUR_API_KEY>"

CONNECTION_PARAMS = {
    "sample_rate": 16000,
    "format_turns": True,
}

API_ENDPOINT = f"wss://streaming.assemblyai.com/v3/ws?{urlencode(CONNECTION_PARAMS)}"
