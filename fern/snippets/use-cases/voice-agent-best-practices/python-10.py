async def handle_streaming_message(data):
    utterance_text = data.get("utterance")
    transcript = data.get("transcript")
    is_final = data.get("end_of_turn")
    turn_order = data.get("turn_order")

    # Check for utterance completion (pre-emptive opportunity)
    if utterance_text:
        # FASTEST: Start LLM processing on complete utterance
        # even though turn hasn't ended
        print(f"🚀 Pre-emptive generation for: '{utterance_text}'")

        # Start async LLM call immediately
        llm_task = asyncio.create_task(
            generate_llm_response(utterance_text, turn_order)
        )

        # Cache for later use
        utterance_cache[turn_order] = {
            "utterance": utterance_text,
            "llm_task": llm_task
        }

    elif is_final:
        # Turn has ended - use pre-computed response if available
        if turn_order in utterance_cache:
            # Response already computing or ready!
            llm_response = await utterance_cache[turn_order]["llm_task"]
            print(f"✅ Using pre-computed response (saved 200-500ms!)")
            return llm_response
        else:
            # Fallback: generate response now
            return await generate_llm_response(transcript, turn_order)

async def generate_llm_response(text, turn_order):
    """Generate LLM response for utterance"""
    response = await llm.complete(
        prompt=f"Respond to: {text}",
        metadata={"turn_order": turn_order}
    )
    return response
