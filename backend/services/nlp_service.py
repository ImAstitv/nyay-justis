import re

def extract_fields(text: str) -> dict:
    fields = {
        "case_id_number": "", "primary_case_nature": "Civil",
        "procedural_stage": "Pre-Trial", "custody_status": "None",
        "immediate_risk": "None", "financial_stake": False,
        "estimated_severity": "Low", "petitioner": "", "respondent": "",
        "under_acts": "", "under_sections": "",
    }
    hits = 0

    patterns = {
        "case_no": r'Case\s*No[:\.\s]+([A-Z0-9/\-]+)',
        "petitioner": r'Petitioner[:\s]+([^\n]+)',
        "respondent": r'Respondent[:\s]+([^\n]+)',
        "under_section": r'Under\s*Section[:\s]+([^\n]+)',
        "under_acts": r'Under\s*Act[:\s]+([^\n]+)',
    }

    m = re.search(patterns["case_no"], text, re.IGNORECASE)
    if m: fields["case_id_number"] = m.group(1).strip(); hits += 1

    m = re.search(patterns["petitioner"], text, re.IGNORECASE)
    if m: fields["petitioner"] = m.group(1).strip()[:200]; hits += 1

    m = re.search(patterns["respondent"], text, re.IGNORECASE)
    if m: fields["respondent"] = m.group(1).strip()[:200]; hits += 1

    m = re.search(patterns["under_section"], text, re.IGNORECASE)
    if m: fields["under_sections"] = m.group(1).strip()[:200]; hits += 1

    m = re.search(patterns["under_acts"], text, re.IGNORECASE)
    if m: fields["under_acts"] = m.group(1).strip()[:200]; hits += 1

    if re.search(r'\bcriminal\b', text, re.IGNORECASE):
        fields["primary_case_nature"] = "Criminal"; hits += 1
    elif re.search(r'\bcivil\b', text, re.IGNORECASE):
        fields["primary_case_nature"] = "Civil"; hits += 1

    if re.search(r'sentencing', text, re.IGNORECASE):
        fields["procedural_stage"] = "Sentencing"; hits += 1
    elif re.search(r'active\s*trial', text, re.IGNORECASE):
        fields["procedural_stage"] = "Active Trial"; hits += 1
    elif re.search(r'pre.?trial', text, re.IGNORECASE):
        fields["procedural_stage"] = "Pre-Trial"; hits += 1

    if re.search(r'judicial custody|remand', text, re.IGNORECASE):
        fields["custody_status"] = "Remand"; hits += 1
    elif re.search(r'bail.*denied|bail.*rejected', text, re.IGNORECASE):
        fields["custody_status"] = "Bail Denied"; hits += 1

    if re.search(r'threat to life|witness intimidation', text, re.IGNORECASE):
        fields["immediate_risk"] = "Threat to Life"; hits += 1
    elif re.search(r'flight risk|absconding', text, re.IGNORECASE):
        fields["immediate_risk"] = "Flight Risk"; hits += 1
    elif re.search(r'livelihood', text, re.IGNORECASE):
        fields["immediate_risk"] = "Loss of Livelihood"; hits += 1

    if re.search(r'severity[:\s]+high|high severity', text, re.IGNORECASE):
        fields["estimated_severity"] = "High"; hits += 1
    elif re.search(r'severity[:\s]+medium', text, re.IGNORECASE):
        fields["estimated_severity"] = "Medium"; hits += 1

    if re.search(r'rs\.|lakhs|crore|property stake|land.*dispute', text, re.IGNORECASE):
        fields["financial_stake"] = True; hits += 1

    confidence = round((hits / 12) * 100)
    return {"fields": fields, "confidence": confidence, "fields_extracted": hits}