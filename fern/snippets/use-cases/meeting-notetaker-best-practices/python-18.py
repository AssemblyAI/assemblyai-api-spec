config = aai.TranscriptionConfig(
    redact_pii=True,
    redact_pii_policies=[
        PIIRedactionPolicy.person_name,      # Remove names
        PIIRedactionPolicy.email_address,    # Remove emails
        PIIRedactionPolicy.phone_number,     # Remove phone numbers
        PIIRedactionPolicy.organization,     # Remove company names
    ],
    redact_pii_sub=PIISubstitutionPolicy.hash,  # Stable hash tokens
)
