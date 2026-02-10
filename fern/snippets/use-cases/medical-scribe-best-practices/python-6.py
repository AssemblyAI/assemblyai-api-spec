# Log all PHI access
def log_phi_access(user_id: str, patient_id: str, action: str):
    """HIPAA requires audit trail of all PHI access"""
    audit_log.write({
        "timestamp": datetime.now(),
        "user_id": user_id,
        "patient_id": patient_id,
        "action": action,  # "transcribe", "view", "edit", "delete"
        "ip_address": request.remote_addr,
    })
