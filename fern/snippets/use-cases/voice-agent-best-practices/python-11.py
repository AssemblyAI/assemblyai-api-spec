# Voice agent with pre-emptive generation
class FastVoiceAgent:
    def __init__(self):
        self.utterance_cache = {}

    async def process_stream(self, data):
        turn_order = data.get("turn_order")
        utterance = data.get("utterance")

        # Log for debugging
        print(f"Turn {turn_order}: utterance='{utterance}' eot={data.get('end_of_turn')}")

        if utterance and not data.get("end_of_turn"):
            # Pre-emptive path: ~300ms head start!
            print(f"⚡ Starting pre-emptive generation for turn {turn_order}")
            self.utterance_cache[turn_order] = asyncio.create_task(
                self.generate_response(utterance)
            )

        if data.get("end_of_turn"):
            # Turn ended - use cached or generate now
            if turn_order in self.utterance_cache:
                response = await self.utterance_cache[turn_order]
                print(f"🎯 Pre-computed response ready instantly!")
            else:
                response = await self.generate_response(data.get("transcript"))
                print(f"⏱️ Generated response on-demand")

            return response
