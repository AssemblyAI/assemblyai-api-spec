def on_message(ws, message):
    """Handle WebSocket messages"""
    try:
        data = json.loads(message)
        msg_type = data.get("type")

        if msg_type == "Begin":
            session_id = data.get("id")
            print(f"Session started: {session_id}")

        elif msg_type == "Turn":
            transcript = data.get("transcript", "")
            if data.get("turn_is_formatted"):
                print(f"Transcript: {transcript}")

        elif msg_type == "Termination":
            # Extract audio duration - this is what you need for billing
            audio_duration_seconds = data.get("audio_duration_seconds", 0)
            session_duration_seconds = data.get("session_duration_seconds", 0)

            print(f"\nSession terminated:")
            print(f"  Audio Duration: {audio_duration_seconds} seconds")
            print(f"  Session Duration: {session_duration_seconds} seconds")

            # Here you would associate audio_duration_seconds with your customer
            # using whatever session management system you have in place
            customer_id = get_customer_id_from_session()  # Your implementation
            log_customer_usage(customer_id, session_duration_seconds)

    except json.JSONDecodeError as e:
        print(f"Error decoding message: {e}")
    except Exception as e:
        print(f"Error handling message: {e}")
