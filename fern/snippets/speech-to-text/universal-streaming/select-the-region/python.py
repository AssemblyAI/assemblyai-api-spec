import websocket
from urllib.parse import urlencode

YOUR_API_KEY = "<YOUR_API_KEY>"
CONNECTION_PARAMS = {"sample_rate": 16000}
API_ENDPOINT_BASE_URL = "wss://streaming.eu.assemblyai.com/v3/ws"
API_ENDPOINT = f"{API_ENDPOINT_BASE_URL}?{urlencode(CONNECTION_PARAMS)}"

ws = websocket.WebSocketApp(
    API_ENDPOINT,
    header={"Authorization": YOUR_API_KEY},
)

ws.run_forever()
