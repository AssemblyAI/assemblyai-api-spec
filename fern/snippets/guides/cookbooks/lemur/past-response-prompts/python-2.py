# Step 2: Define the initial prompt.
initial_prompt = input("Enter the initial prompt: ")

# Step 3: Apply LeMUR.
result = transcript.lemur.task(initial_prompt)

# Step 4: Store result in a list.
results_list = [result.response]

print(result.response)
