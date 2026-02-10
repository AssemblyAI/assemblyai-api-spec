class TranscriptProcessor:
    def __init__(self):
        self.current_turn = 0
        self.pre_computed_responses = {}

    async def process_message(self, data):
        msg_type = data.get("type")

        if msg_type == "Begin":
            print(f"Session started: {data.get('id')}")

        elif msg_type == "Turn":
            return await self.process_turn(data)

        elif msg_type == "Termination":
            print(f"Session ended: {data.get('message')}")

    async def process_turn(self, data):
        turn_order = data.get("turn_order")
        transcript = data.get("transcript")
        utterance = data.get("utterance")
        is_final = data.get("end_of_turn")
        eot_confidence = data.get("end_of_turn_confidence", 0)

        # Track turn changes
        if turn_order != self.current_turn:
            self.current_turn = turn_order
            print(f"\n🔄 New turn #{turn_order}")

        # Monitor progress
        print(f"  Confidence: {eot_confidence:.3f} | Transcript: '{transcript}'")

        # KEY: Check for utterance completion (pre-emptive opportunity)
        if utterance:
            print(f"  ⚡ UTTERANCE COMPLETE: '{utterance}' - Starting pre-generation!")

            # Start LLM processing immediately
            self.pre_computed_responses[turn_order] = asyncio.create_task(
                self.generate_response(utterance)
            )

        # Handle turn completion
        if is_final:
            print(f"  ✅ TURN COMPLETE: '{transcript}'")

            # Use pre-computed response if available
            if turn_order in self.pre_computed_responses:
                response = await self.pre_computed_responses[turn_order]
                print(f"  🎯 Using pre-computed response (instant!)")
            else:
                response = await self.generate_response(transcript)
                print(f"  ⏱️ Generating response now")

            return response

    async def generate_response(self, text):
        # Your LLM call
        return f"Response to: {text}"
