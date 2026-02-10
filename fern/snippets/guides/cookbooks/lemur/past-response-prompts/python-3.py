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
