from datetime import datetime

VULNERABILITY_MAP = {
    "murder": 3.0, "culpable homicide": 3.0, "302": 3.0,
    "rape": 3.0, "376": 3.0, "pocso": 3.0,
    "kidnapping": 2.5, "363": 2.5, "364": 2.5,
    "domestic violence": 2.5, "sc/st": 2.5, "atrocities": 2.5,
    "land acquisition": 2.0, "succession": 2.0, "maintenance": 2.0,
    "motor accident": 1.8, "cheque bounce": 1.5, "138": 1.5,
    "contract": 1.2,
}

STAGE_MAP = {
    "sentencing": 3.0, "arguments": 2.5, "evidence": 2.2,
    "active trial": 2.0, "framing of charges": 1.8,
    "pre-trial": 1.5, "awaiting for l.c.r.": 1.3,
}

IPC_MAX_DAYS = {
    "302": 365 * 20, "376": 365 * 10, "307": 365 * 10,
    "363": 365 * 7, "420": 365 * 7, "379": 365 * 3,
    "138": 365 * 2, "406": 365 * 3,
}

OMEGA_THRESHOLD = 10

def get_vulnerability(under_acts: str, under_sections: str,
                      primary_case_nature: str, immediate_risk: str,
                      custody_status: str, estimated_severity: str) -> float:
    combined = f"{under_acts or ''} {under_sections or ''}".lower()
    for keyword, score in VULNERABILITY_MAP.items():
        if keyword in combined:
            return score
    # Fallback to legacy fields
    v = 1.0
    if primary_case_nature == "Criminal": v = max(v, 2.0)
    if immediate_risk == "Threat to Life": v = max(v, 2.5)
    elif immediate_risk == "Flight Risk": v = max(v, 1.8)
    elif immediate_risk == "Loss of Livelihood": v = max(v, 1.5)
    if custody_status in ["Remand", "Bail Denied"]: v = max(v, 1.8)
    if estimated_severity == "High": v = max(v, 1.5)
    elif estimated_severity == "Medium": v = max(v, 1.2)
    return v

def get_stage_coeff(stage: str) -> float:
    s = (stage or "").lower()
    for key, val in STAGE_MAP.items():
        if key in s:
            return val
    return 1.0

def check_436a(under_sections: str, days_in_custody: int) -> dict:
    for section, max_days in IPC_MAX_DAYS.items():
        if section in (under_sections or ""):
            threshold = max_days / 2
            if days_in_custody >= threshold:
                return {
                    "eligible": True,
                    "section": section,
                    "days_in_custody": days_in_custody,
                    "threshold": int(threshold),
                    "message": f"Section 436A: Accused has served {days_in_custody} days. Bail must be considered."
                }
    return {"eligible": False}

def compute_priority(case) -> dict:
    filing = case.filing_date
    if hasattr(filing, 'date'):
        A = (datetime.utcnow().date() - filing.date()).days
    else:
        A = 0
    A = max(A, 0)
    F = case.friction_index or 0
    V = get_vulnerability(
        case.under_acts, case.under_sections,
        case.primary_case_nature, case.immediate_risk,
        case.custody_status, case.estimated_severity
    )
    C = get_stage_coeff(case.current_stage)
    omega = F > OMEGA_THRESHOLD
    P = round((0.1 * A) + (5.0 * F * V * C) + (500 if omega else 0), 2)

    # Undertrial override — always critical
    s436a = check_436a(case.under_sections or "", case.days_in_custody or 0)

    if P >= 200 or omega:
        band = "High Priority"
        citizen_msg = "Your case has been flagged as high priority. An early hearing is likely."
    elif P >= 80:
        band = "Medium Priority"
        citizen_msg = "Your case is in active queue and will be scheduled based on availability."
    else:
        band = "Low Priority"
        citizen_msg = "Your case is registered and queued. You will be notified when a date is assigned."

    judge_explanation = (
        f"Aging: {A} days → +{round(0.1*A,1)} | "
        f"Adjournments: {F} × V({V}) × C({C}) → +{round(5.0*F*V*C,1)}"
        + (" | ⚠️ OMEGA: Anti-starvation +500" if omega else "")
    )

    return {
        "priority_score": P,
        "aging_factor": float(A),
        "vulnerability": V,
        "stage_coeff": C,
        "omega_flag": omega,
        "band": band,
        "judge_explanation": judge_explanation,
        "citizen_summary": citizen_msg,
        "section_436a": s436a,
    }