# Parse WebSocket data (same as dial-in)
transport_type, call_data = await parse_telephony_websocket(websocket)

# Extract call information
stream_id = call_data["stream_id"]
call_control_id = call_data["call_control_id"]
from_number = call_data["from"]  # Your Telnyx number
to_number = call_data["to"]      # Target number you're calling

# Customize bot behavior for outbound calls
greeting = f"Hi! This is an automated call from {from_number}. How are you today?"
