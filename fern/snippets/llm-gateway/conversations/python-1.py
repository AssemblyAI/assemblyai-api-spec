# First exchange
messages = [
    {"role": "user", "content": "What is the capital of France?"}
]
# Response: "The capital of France is Paris."

# Second exchange - model remembers Paris
messages = [
    {"role": "user", "content": "What is the capital of France?"},
    {"role": "assistant", "content": "The capital of France is Paris."},
    {"role": "user", "content": "What's the population?"}
]
# Response: "As of the latest estimates, the population of Paris is approximately 2.2 million..."
