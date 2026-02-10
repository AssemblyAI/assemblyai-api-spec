import requests
import json
import os
import csv
import time
import re

# Configuration
api_key = "<YOUR_API_KEY>"
base_url = "https://api.assemblyai.com"
headers = {"authorization": api_key}
output_filename = "profiles.csv"

def extract_json(text):
    """Extract JSON from text that might contain markdown or extra text"""
    # First, try to remove markdown code blocks
    text = text.strip()

    # Remove ```json and ``` markers
    if text.startswith("```"):
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)

    # Find the first { and last } to extract just the JSON object
    first_brace = text.find('{')
    last_brace = text.rfind('}')

    if first_brace != -1 and last_brace != -1:
        json_str = text[first_brace:last_brace + 1]
        return json.loads(json_str)

    # If that didn't work, try parsing the whole thing
    return json.loads(text)

def upload_file(file_path):
    """Upload a local audio file to AssemblyAI"""
    with open(file_path, "rb") as f:
        response = requests.post(f"{base_url}/v2/upload", headers=headers, data=f)
        if response.status_code != 200:
            print(f"Error uploading {file_path}: {response.status_code}, {response.text}")
            response.raise_for_status()
        return response.json()["upload_url"]

def transcribe_audio(audio_url):
    """Submit audio for transcription and poll until complete"""
    # Submit transcription request
    data = {"audio_url": audio_url}
    response = requests.post(f"{base_url}/v2/transcript", headers=headers, json=data)

    if response.status_code != 200:
        print(f"Error submitting transcription: {response.status_code}, {response.text}")
        response.raise_for_status()

    transcript_id = response.json()["id"]
    polling_endpoint = f"{base_url}/v2/transcript/{transcript_id}"

    # Poll for completion
    while True:
        transcript = requests.get(polling_endpoint, headers=headers).json()
        if transcript["status"] == "completed":
            return transcript["text"]
        elif transcript["status"] == "error":
            raise RuntimeError(f"Transcription failed: {transcript['error']}")
        else:
            time.sleep(3)

def process_with_llm_gateway(transcript_text, prompt):
    """Send transcript to LLM Gateway for processing"""
    llm_gateway_data = {
        "model": "claude-sonnet-4-5-20250929",
        "messages": [
            {
                "role": "user",
                "content": f"{prompt}\n\nTranscript:\n\n{transcript_text}"
            }
        ],
        "max_tokens": 1500
    }

    response = requests.post(
        "https://llm-gateway.assemblyai.com/v1/chat/completions",
        headers=headers,
        json=llm_gateway_data
    )

    result = response.json()

    if "error" in result:
        raise RuntimeError(f"LLM Gateway error: {result['error']}")

    return result['choices'][0]['message']['content']

# Main execution
prompt = """
        You are an HR executive scanning through an interview transcript to extract information about a candidate.
        You are required to create a JSON response with key information about the candidate.
        You will use this template for your answer:
        {
            "Name": "<candidate-name>",
            "Position": "<job position that candidate is applying for>",
            "Past experience": "<A short phrase describing the candidate's relevant past experience for the role>"
        }
        Do not include any other text in your response. Only respond in JSON format that is not surrounded by markdown code, as your response will be parsed programmatically as JSON.
        """

# Get all files from interviews directory
interview_files = [os.path.join("interviews", file) for file in os.listdir("interviews")]

with open(output_filename, "w", newline="") as file:
    writer = csv.writer(file)
    header = ["Name", "Position", "Past Experience"]
    writer.writerow(header)

    print(f"Processing {len(interview_files)} interview files...")

    for interview_file in interview_files:
        print(f"\nProcessing: {interview_file}")

        # Upload file and get URL
        print("  Uploading file...")
        audio_url = upload_file(interview_file)

        # Transcribe audio
        print("  Transcribing...")
        transcript_text = transcribe_audio(audio_url)

        # Process with LLM Gateway
        print("  Analyzing with LLM Gateway...")
        llm_response = process_with_llm_gateway(transcript_text, prompt)

        # Parse JSON response
        interviewee_data = extract_json(llm_response)
        writer.writerow(interviewee_data.values())
        print(f"  Completed: {interviewee_data['Name']}")

print(f"\nCreated .csv file {output_filename}")
