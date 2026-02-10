# Define questions for each SOAP section
questions = [
    {
        "section": "Subjective",
        "question": "What are the patient's current symptoms or concerns?",
        "context": "Gather information about the patient's subjective experience. Example: The patient reports experiencing persistent headaches and dizziness.",
        "format": "<patient's symptoms or concerns>, [exact quote from patient]"
    },
    {
        "section": "Objective",
        "question": "What are the measurable and observable findings from the examination?",
        "context": "Collect data on the patient's objective signs and measurements. Example: The examination reveals an elevated body temperature and increased heart rate.",
        "format": "<measurable and observable findings>"
    },
    {
        "section": "Assessment",
        "question": "Based on the patient's history and examination, what is your assessment or diagnosis?",
        "context": "Formulate a professional assessment based on the gathered information. Example: Based on the patient's symptoms, examination, and medical history, the preliminary diagnosis is migraine.",
        "format": "<assessment or diagnosis>"
    },
    {
        "section": "Plan",
        "question": "What is the plan of action or treatment for the patient?",
        "context": "Outline the intended course of action or treatment. Example: The treatment plan includes prescribing medication, recommending rest, and scheduling a follow-up appointment in two weeks.",
        "format": "<plan of action or treatment>, [exact quote from provider]"
    }
]

# Process each section
for q in questions:
    prompt = f"""
{q['question']}

Context: This is a doctor appointment between patient and provider. The personal identification information has been redacted. {q['context']}

Answer Format: {q['format']}
"""

    llm_gateway_data = {
        "model": "claude-sonnet-4-5-20250929",
        "messages": [
            {"role": "user", "content": f"{prompt}\n\nTranscript: {transcription_result['text']}"}
        ],
        "max_tokens": 1000
    }

    response = requests.post(
        "https://llm-gateway.assemblyai.com/v1/chat/completions",
        headers=headers,
        json=llm_gateway_data
    )

    result = response.json()["choices"][0]["message"]["content"]
    print(f"{q['section']}: {q['question']}")
    print(result.strip())
    print()
