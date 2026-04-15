"""
Run: python seed_data.py
Seeds 50 realistic Danapur Civil Court cases.
Safe to run multiple times — checks for existing CNRs.
"""
import requests
import random
from datetime import datetime, timedelta

API = "http://127.0.0.1:8000"

# Get token first
token_res = requests.post(f"{API}/auth/login", data={"username": "judge", "password": "judge123"})
TOKEN = token_res.json()["access_token"]
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

CASE_TYPES = ["CRM", "CIV", "TS", "TA", "MA"]
STAGES = ["Pre-Trial", "Framing of Charges", "Evidence", "Arguments", "Active Trial", "Sentencing"]
ACTS = ["Indian Penal Code", "Indian Succession Act", "Transfer of Property Act",
        "Negotiable Instruments Act", "POCSO Act", "SC/ST Atrocities Act",
        "Domestic Violence Act", "Motor Vehicles Act"]
SECTIONS = [["302", "34"], ["376"], ["138"], ["420", "406"], ["307"], ["363"], ["498A"]]
RISKS = ["None", "None", "None", "Flight Risk", "Threat to Life", "Loss of Livelihood"]
PETITIONERS = ["State of Bihar", "Ram Prasad", "Sita Devi", "Mohan Lal",
                "Kavita Sharma", "District Collector", "Bihar State Electricity Board"]
RESPONDENTS = ["Ramesh Kumar", "Suresh Singh", "Priya Mishra", "Anil Yadav",
               "Sunita Devi", "Raj Kumar Gupta", "Bihar Roads Corp"]

def random_date(years_back=8):
    days = random.randint(30, years_back * 365)
    return datetime.now() - timedelta(days=days)

seeded = 0
for i in range(1, 51):
    prefix = random.choice(CASE_TYPES)
    year = random.choice([2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024])
    cnr = f"{prefix}/{year}/{i:04d}"
    sections = random.choice(SECTIONS)
    nature = "Criminal" if prefix in ["CRM", "TS"] else "Civil"
    is_undertrial = nature == "Criminal" and random.random() < 0.3
    days_custody = random.randint(30, 900) if is_undertrial else 0

    payload = {
        "case_id_number": cnr,
        "primary_case_nature": nature,
        "procedural_stage": random.choice(STAGES),
        "custody_status": random.choice(["None", "None", "Remand", "Bail Denied"]),
        "immediate_risk": random.choice(RISKS),
        "financial_stake": random.choice([True, False, False]),
        "estimated_severity": random.choice(["Low", "Low", "Medium", "High"]),
        "petitioner": random.choice(PETITIONERS),
        "respondent": random.choice(RESPONDENTS),
        "under_acts": random.choice(ACTS),
        "under_sections": "/".join(sections),
        "is_undertrial": is_undertrial,
        "days_in_custody": days_custody,
    }

    # Simulate adjournments by calling adjourn endpoint after creating
    r = requests.post(f"{API}/cases", json=payload, headers=HEADERS)
    if r.status_code == 200:
        case_id = r.json().get("id")
        adj_count = random.randint(0, 15)
        for _ in range(adj_count):
            requests.put(f"{API}/cases/{case_id}/adjourn",
                        params={"reason": random.choice([
                            "Respondent's advocate absent",
                            "Petitioner sought time",
                            "Court holiday",
                            "Judge on leave",
                            "Documents not filed"
                        ])},
                        headers=HEADERS)
        seeded += 1
        print(f"[{seeded}/50] Seeded {cnr} — {adj_count} adjournments")
    else:
        print(f"Skip {cnr}: {r.text[:60]}")

print(f"\nDone. {seeded} cases seeded.")