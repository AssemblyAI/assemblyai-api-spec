import assemblyai

assemblyai.settings.api_key = "YOUR_API_KEY"
transcriber = assemblyai.Transcriber()

transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/5_common_sports_injuries.mp3") # You can also replace this with the path to a local file

# Define the initial prompt.
initial_prompt = input("Enter the initial prompt: ")

# Apply LeMUR.
result = transcript.lemur.task(initial_prompt)

# Store result in a list.
results_list = [result.response]

print(result.response)

while True:
    user_prompt = input("Enter the next prompt (or type 'end' to stop): ")

    if user_prompt.lower() == 'end':
        print("Ending the conversation.")
        break

    context = " ".join(results_list)
    next_prompt = f"{user_prompt} (Context: {context})"

    next_result = transcript.lemur.task(next_prompt, final_model=assemblyai.LemurModel.claude3_5_sonnet)

    results_list.append(next_result.response)

    print(next_result.response)
