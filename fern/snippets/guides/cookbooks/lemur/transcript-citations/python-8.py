print("Asking LLM Gateway for best quotes...")
question = "What are the 3 best quotes from this video?"
context = "Please provide exactly 3 quotes."

llm_answer = process_with_llm_gateway(transcript_text, question, context)
print(f"\nLLM Gateway Response:\n{llm_answer}\n")
