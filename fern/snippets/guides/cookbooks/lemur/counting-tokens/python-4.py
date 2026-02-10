# Define your prompt
prompt = "Provide a brief summary of the transcript."

# Calculate character count (transcript + prompt)
transcript_chars = len(transcript["text"])
prompt_chars = len(prompt)
total_chars = transcript_chars + prompt_chars
print(f"\nTotal characters: {total_chars}")
