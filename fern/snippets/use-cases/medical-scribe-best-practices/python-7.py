import requests
import json
from typing import Dict, List, Optional

class MedicalSOAPGenerator:
    """Generate structured SOAP notes from medical transcripts using LLM Gateway"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://llm-gateway.assemblyai.com/v1/chat/completions"
        self.headers = {"authorization": api_key}

    def generate_soap_note(self,
                          transcript: str,
                          patient_context: Optional[Dict] = None,
                          visit_type: str = "general") -> Dict:
        """Generate SOAP note from medical transcript"""

        # Build context for the LLM
        context_prompt = self._build_context_prompt(transcript, patient_context, visit_type)

        messages = [
            {
                "role": "system",
                "content": """You are a clinical documentation specialist. Generate a structured SOAP note from the medical encounter transcript.

SOAP Format:
- Subjective: Patient's chief complaint, history of present illness, and symptoms
- Objective: Provider's observations, physical exam findings, vital signs, and test results
- Assessment: Provider's clinical impressions, diagnoses, and differential diagnoses
- Plan: Treatment recommendations, medications, follow-up instructions, and referrals

Guidelines:
- Use medical terminology appropriately
- Include specific details mentioned in the encounter
- Maintain clinical accuracy
- Use bullet points for clarity
- Include medications with dosages and frequencies
- Note any follow-up appointments or referrals"""
            },
            {
                "role": "user",
                "content": context_prompt
            }
        ]

        response = requests.post(
            self.base_url,
            headers=self.headers,
            json={
                "model": "claude-sonnet-4-5-20250929",  # Best for medical reasoning
                "messages": messages,
                "max_tokens": 2000,
                "temperature": 0.1  # Low temperature for consistent medical documentation
            }
        )

        if response.status_code == 200:
            result = response.json()
            soap_content = result["choices"][0]["message"]["content"]

            return {
                "soap_note": soap_content,
                "structured_data": self._extract_structured_data(soap_content),
                "visit_type": visit_type,
                "generation_timestamp": self._get_timestamp()
            }
        else:
            raise Exception(f"LLM Gateway error: {response.status_code} - {response.text}")

    def _build_context_prompt(self, transcript: str, patient_context: Optional[Dict], visit_type: str) -> str:
        """Build comprehensive context prompt for SOAP generation"""

        prompt_parts = [
            f"Generate a SOAP note for a {visit_type} medical encounter.",
            "",
            "MEDICAL ENCOUNTER TRANSCRIPT:",
            transcript,
            ""
        ]

        if patient_context:
            prompt_parts.extend([
                "PATIENT CONTEXT:",
                f"- Age: {patient_context.get('age', 'Not specified')}",
                f"- Known conditions: {', '.join(patient_context.get('conditions', []))}",
                f"- Current medications: {', '.join(patient_context.get('medications', []))}",
                f"- Allergies: {', '.join(patient_context.get('allergies', []))}",
                ""
            ])

        prompt_parts.extend([
            "Please generate a comprehensive SOAP note following the format:",
            "Subjective:",
            "Objective:",
            "Assessment:",
            "Plan:",
            "",
            "Include specific details, medications with dosages, and any follow-up instructions mentioned."
        ])

        return "\n".join(prompt_parts)

    def _extract_structured_data(self, soap_content: str) -> Dict:
        """Extract structured data from SOAP note"""

        sections = {
            "subjective": self._extract_section(soap_content, "Subjective"),
            "objective": self._extract_section(soap_content, "Objective"),
            "assessment": self._extract_section(soap_content, "Assessment"),
            "plan": self._extract_section(soap_content, "Plan")
        }

        return {
            "sections": sections,
            "medications": self._extract_medications(soap_content),
            "diagnoses": self._extract_diagnoses(soap_content),
            "follow_up": self._extract_follow_up(soap_content)
        }

    def _extract_section(self, content: str, section_name: str) -> str:
        """Extract specific SOAP section"""
        import re

        pattern = rf"{section_name}:\s*(.*?)(?=\n\w+:|$)"
        match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def _extract_medications(self, content: str) -> List[str]:
        """Extract medication mentions from SOAP note"""
        import re

        # Look for medication patterns
        medication_patterns = [
            r"([A-Z][a-z]+(?:mycin|pril|sartan|pine|zole|statin|pam|zepam))\s+\d+\s*mg",
            r"([A-Z][a-z]+)\s+\d+\s*mg\s+(?:daily|twice daily|BID|TID|QID)",
            r"([A-Z][a-z]+)\s+\d+\s*mg\s+(?:once|twice|three times)\s+(?:daily|a day)"
        ]

        medications = []
        for pattern in medication_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            medications.extend(matches)

        return list(set(medications))  # Remove duplicates

    def _extract_diagnoses(self, content: str) -> List[str]:
        """Extract diagnosis mentions from Assessment section"""
        assessment = self._extract_section(content, "Assessment")

        # Common diagnosis patterns
        diagnosis_patterns = [
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+(?:syndrome|disease|disorder|condition)",
            r"(?:diagnosis|impression):\s*([^,\n]+)",
            r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+likely"
        ]

        diagnoses = []
        for pattern in diagnosis_patterns:
            matches = re.findall(pattern, assessment, re.IGNORECASE)
            diagnoses.extend(matches)

        return list(set(diagnoses))

    def _extract_follow_up(self, content: str) -> List[str]:
        """Extract follow-up instructions from Plan section"""
        plan = self._extract_section(content, "Plan")

        follow_up_patterns = [
            r"follow[-\s]up\s+in\s+([^,\n]+)",
            r"return\s+in\s+([^,\n]+)",
            r"recheck\s+in\s+([^,\n]+)",
            r"schedule\s+([^,\n]+)"
        ]

        follow_ups = []
        for pattern in follow_up_patterns:
            matches = re.findall(pattern, plan, re.IGNORECASE)
            follow_ups.extend(matches)

        return list(set(follow_ups))

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()

# Example usage
async def generate_clinical_documentation(audio_file: str, patient_id: str):
    """Complete workflow: transcribe + generate SOAP note"""

    config = aai.TranscriptionConfig(
        speech_model=aai.SpeechModel.universal_3_pro,
        speaker_labels=True,
        speakers_expected=2,
        keyterms_prompt=get_patient_medical_history(patient_id),
        entity_detection=True,
        redact_pii=True,
        redact_pii_policies=[...],  # All HIPAA identifiers
    )

    transcript = await transcribe_async(audio_file, config)

    # Step 2: Load patient context from EHR
    patient_context = ehr.get_patient(patient_id)

    # Step 3: Generate SOAP note using LLM Gateway
    soap_generator = MedicalSOAPGenerator(api_key="your_api_key")

    soap_result = soap_generator.generate_soap_note(
        transcript=transcript.text,
        patient_context={
            "age": patient_context.get("age"),
            "conditions": [c.name for c in patient_context.get("conditions", [])],
            "medications": [f"{m.name} {m.dosage}" for m in patient_context.get("medications", [])],
            "allergies": [a.name for a in patient_context.get("allergies", [])]
        },
        visit_type="primary_care_followup"
    )

    # Step 4: Update EHR with structured data
    ehr.update_patient_record(patient_id, {
        "soap_note": soap_result["soap_note"],
        "medications_mentioned": soap_result["structured_data"]["medications"],
        "diagnoses": soap_result["structured_data"]["diagnoses"],
        "follow_up_instructions": soap_result["structured_data"]["follow_up"]
    })

    return {
        "transcript": transcript,
        "soap_note": soap_result["soap_note"],
        "structured_data": soap_result["structured_data"],
        "clinical_entities": transcript.entities
    }

# Example output
"""
Subjective:
- Patient presents with chest pain for 3 days
- Pain is substernal, 7/10 intensity, radiating to left arm
- Associated with shortness of breath and diaphoresis
- No relief with rest or nitroglycerin
- History of hypertension and diabetes mellitus type 2

Objective:
- Vital signs: BP 160/95, HR 95, RR 22, O2 sat 94% on room air
- Physical exam: Diaphoretic, mild distress
- Heart: Regular rate and rhythm, no murmurs
- Lungs: Clear bilaterally
- Extremities: No edema

Assessment:
- Acute coronary syndrome, rule out STEMI
- Hypertension, poorly controlled
- Diabetes mellitus type 2, stable

Plan:
- STAT EKG and troponin levels
- Aspirin 325mg daily
- Atorvastatin 80mg at bedtime
- Cardiology consultation
- Follow up in 1 week
- Return to ED if chest pain worsens
"""
