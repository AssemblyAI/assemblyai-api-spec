class AdvancedSOAPGenerator(MedicalSOAPGenerator):
    """Enhanced SOAP generator with specialty-specific templates"""

    def generate_specialty_soap(self, transcript: str, specialty: str, patient_context: Dict) -> Dict:
        """Generate specialty-specific SOAP notes"""

        specialty_templates = {
            "cardiology": self._cardiology_template(),
            "endocrinology": self._endocrinology_template(),
            "oncology": self._oncology_template(),
            "psychiatry": self._psychiatry_template()
        }

        template = specialty_templates.get(specialty, self._general_template())

        messages = [
            {
                "role": "system",
                "content": f"""You are a {specialty} specialist. Generate a detailed SOAP note using this template:

                {template}

                Focus on {specialty}-specific terminology, assessments, and treatment plans."""
            },
            {
                "role": "user",
                "content": f"Generate a {specialty} SOAP note for this encounter:\n\n{transcript}"
            }
        ]

        response = requests.post(
            self.base_url,
            headers=self.headers,
            json={
                "model": "claude-sonnet-4-5-20250929",
                "messages": messages,
                "max_tokens": 2500,
                "temperature": 0.1
            }
        )

        return response.json()

    def _cardiology_template(self) -> str:
        return """
        Subjective:
        - Chief complaint and cardiac history
        - Chest pain characteristics (quality, location, radiation, timing)
        - Dyspnea, orthopnea, paroxysmal nocturnal dyspnea
        - Palpitations, syncope, presyncope
        - Risk factors (smoking, diabetes, hypertension, family history)

        Objective:
        - Vital signs including orthostatic vitals
        - Cardiovascular exam (heart sounds, murmurs, gallops)
        - Peripheral vascular exam (pulses, edema, JVD)
        - Relevant lab values (troponin, BNP, lipids)
        - Imaging results (EKG, echo, stress test, cath)

        Assessment:
        - Primary cardiac diagnosis
        - Secondary diagnoses
        - Risk stratification (Framingham, ASCVD)

        Plan:
        - Medications with cardiac indications
        - Procedures (cath, echo, stress test)
        - Lifestyle modifications
        - Follow-up and monitoring
        """

    def _endocrinology_template(self) -> str:
        return """
        Subjective:
        - Diabetes symptoms (polyuria, polydipsia, weight changes)
        - Thyroid symptoms (fatigue, weight changes, heat/cold intolerance)
        - Medication adherence and side effects
        - Blood glucose monitoring results

        Objective:
        - Vital signs including BMI
        - Thyroid exam
        - Diabetic foot exam
        - Lab values (HbA1c, glucose, thyroid function)

        Assessment:
        - Diabetes control and complications
        - Thyroid function status
        - Endocrine disorders

        Plan:
        - Medication adjustments
        - Lab monitoring schedule
        - Patient education
        - Specialist referrals
        """

# Usage example for specialty SOAP notes
async def generate_cardiology_soap(transcript: str, patient_id: str):
    """Generate cardiology-specific SOAP note"""

    generator = AdvancedSOAPGenerator(api_key="your_api_key")

    patient_context = ehr.get_patient(patient_id)

    soap_result = generator.generate_specialty_soap(
        transcript=transcript,
        specialty="cardiology",
        patient_context=patient_context
    )

    return soap_result
