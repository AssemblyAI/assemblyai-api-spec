import requests
import time

base_url = "https://api.assemblyai.com"
headers = {"authorization": "YOUR_API_KEY"}

# Transcribe audio file
audio_url = "https://assembly.ai/wildfires.mp3"
data = {"audio_url": audio_url}

response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)
transcript_id = response.json()["id"]
polling_endpoint = base_url + f"/v2/transcript/{transcript_id}"

# Poll for completion
print("Waiting for transcription to complete...")

while True:
    transcript = requests.get(polling_endpoint, headers=headers).json()
    if transcript["status"] == "completed":
        break
    elif transcript["status"] == "error":
        raise RuntimeError(f"Transcription failed: {transcript['error']}")
    time.sleep(3)

# Define your prompt
prompt = "Provide a brief summary of the transcript."

# Calculate character count (transcript + prompt)
transcript_chars = len(transcript["text"])
prompt_chars = len(prompt)
total_chars = transcript_chars + prompt_chars
print(f"\nTotal characters: {total_chars}")

# Estimate tokens (roughly 4 characters = 1 token)
estimated_tokens = total_chars / 4
tokens_in_millions = estimated_tokens / 1_000_000

# Calculate input costs for different models
gpt5_cost = 1.25 * tokens_in_millions
claude_sonnet_cost = 3.00 * tokens_in_millions
gemini_pro_cost = 1.25 * tokens_in_millions

print(f"Estimated input tokens: {estimated_tokens:,.0f}")
print(f"\nEstimated input costs:")
print(f"GPT-5: ${gpt5_cost:.4f}")
print(f"Claude 4.5 Sonnet: ${claude_sonnet_cost:.4f}")
print(f"Gemini 2.5 Pro: ${gemini_pro_cost:.4f}")
