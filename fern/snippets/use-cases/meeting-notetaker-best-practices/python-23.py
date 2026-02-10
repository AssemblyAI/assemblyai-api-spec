class StreamingResponseProcessor:
    def __init__(self):
        self.partial_buffer = ""
        self.final_transcripts = []
        self.turn_metadata = []

    def process_message(self, message: dict):
        """
        Process real-time streaming messages
        """
        msg_type = message.get("type")

        if msg_type == "Begin":
            return {
                "event": "session_started",
                "session_id": message.get("id"),
                "expires_at": message.get("expires_at")
            }

        elif msg_type == "Turn":
            return self.process_turn(message)

        elif msg_type == "Termination":
            return {
                "event": "session_ended",
                "audio_duration": message.get("audio_duration_seconds"),
                "session_duration": message.get("session_duration_seconds")
            }

    def process_turn(self, data: dict):
        """Process turn messages"""
        is_final = data.get("end_of_turn")
        is_formatted = data.get("turn_is_formatted")
        transcript = data.get("transcript", "")
        turn_order = data.get("turn_order")

        response = {
            "turn_order": turn_order,
            "is_final": is_final,
            "is_formatted": is_formatted,
            "confidence": data.get("end_of_turn_confidence", 0)
        }

        # Handle partials (for live display)
        if not is_final and transcript:
            self.partial_buffer = transcript
            response["event"] = "partial"
            response["text"] = transcript

        # Handle finals (for storage)
        elif is_final and is_formatted:
            final_transcript = {
                "turn_order": turn_order,
                "text": transcript,
                "confidence": data.get("end_of_turn_confidence"),
                "timestamp": datetime.now().isoformat()
            }
            self.final_transcripts.append(final_transcript)
            response["event"] = "final"
            response["text"] = transcript

            # Clear partial buffer
            self.partial_buffer = ""

        return response

    def get_full_transcript(self):
        """
        Combine all final transcripts into complete meeting transcript
        """
        return {
            "full_text": " ".join(t["text"] for t in self.final_transcripts),
            "transcripts": self.final_transcripts,
            "total_turns": len(self.final_transcripts)
        }

# Example usage
processor = StreamingResponseProcessor()

# If you're using `websockets` version 13.0 or later, use `additional_headers` parameter. For older versions (< 13.0), use `extra_headers` instead.
async with websockets.connect(API_ENDPOINT, additional_headers=headers) as ws:
    async for message in ws:
        data = json.loads(message)
        result = processor.process_message(data)

        if result["event"] == "partial":
            # Update UI with live transcript
            update_live_caption(result["text"])

        elif result["event"] == "final":
            # Save final transcript
            save_transcript_segment(result)

# Get complete transcript when done
full_transcript = processor.get_full_transcript()
