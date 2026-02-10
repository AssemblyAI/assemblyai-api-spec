config = aai.TranscriptionConfig(
    # HIPAA-mandated PII redaction
    redact_pii=True,
    redact_pii_policies=[
        # All 18 HIPAA identifiers
        PIIRedactionPolicy.person_name,              # Patient & provider names
        PIIRedactionPolicy.date_of_birth,            # DOB
        PIIRedactionPolicy.date,                     # All dates (except year)
        PIIRedactionPolicy.phone_number,             # Phone numbers
        PIIRedactionPolicy.email_address,            # Email addresses
        PIIRedactionPolicy.medical_record_number,    # MRN, account numbers
        PIIRedactionPolicy.social_security_number,   # SSN
        PIIRedactionPolicy.account_number,           # Financial accounts
        PIIRedactionPolicy.certificate_number,       # License numbers
        PIIRedactionPolicy.vehicle_identifier,       # License plates, VINs
        PIIRedactionPolicy.device_identifier,        # Serial numbers
        PIIRedactionPolicy.web_url,                  # URLs
        PIIRedactionPolicy.ip_address,               # IP addresses
        PIIRedactionPolicy.biometric_identifier,     # Fingerprints, voiceprints
        PIIRedactionPolicy.face_identifier,          # Facial photos
        PIIRedactionPolicy.other_identifier,         # Any other unique identifiers
    ],
    redact_pii_sub=PIISubstitutionPolicy.hash,  # Use stable hash tokens
    redact_pii_audio=True,  # Create de-identified audio file
)
