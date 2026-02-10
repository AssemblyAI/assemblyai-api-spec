def on_message(ws, message):
    try:
        msg = json.loads(message)
        msg_type = msg.get('message_type')

        if msg_type == 'SessionBegins':
            session_id = msg.get('session_id')
            print("Session ID:", session_id)
            return

        text = msg.get('text', '')
        if not text:
            return

        if msg_type == 'PartialTranscript':
            print(text, end='\r')
        elif msg_type == 'FinalTranscript':
            print(text, end='\r\n')
        elif msg_type == 'error':
            print(f'\nError: {msg.get("error", "Unknown error")}')
    except Exception as e:
        print(f'\nError handling message: {e}')
