prompt = """
Generate a SOAP note summary based on the following doctor-patient appointment transcript.

Context: This is a doctor appointment between patient and provider. The personal identification information has been redacted.

Format the response as follows:

Subjective
This is typically the shortest section (only 2-3 sentences) and it describes the patient's affect, as the professional sees it. This information is all subjective (it isn't measureable).
- Include information that may have affected the patient's performance, such as if they were sick, tired, attentive, distractible, etc.
- Was the patient on time or did they come late?
- May include a quote of something the patient said, or how they reported feeling

Objective
This section includes factual, measurable, and objective information. This may include:
- Direct patient quotes
- Measurements
- Data on patient performance

Assessment
This section should be the meat of the SOAP note. It contains a narrative of what actually happened during the session. There may be information regarding:
- Whether improvements have been made since the last session
- Any potential barriers to success
- Clinician's interpretation of the results of the session

Plan
This is another short section that states the plan for future sessions. In most settings, this section may be bulleted
"""

# Send to LLM Gateway
llm_gateway_data = {
    "model": "claude-sonnet-4-5-20250929",
    "messages": [
        {"role": "user", "content": f"{prompt}\n\nTranscript: {transcription_result['text']}"}
    ],
    "max_tokens": 2000
}

response = requests.post(
    "https://llm-gateway.assemblyai.com/v1/chat/completions",
    headers=headers,
    json=llm_gateway_data
)

result = response.json()["choices"][0]["message"]["content"]
print(result.strip())
