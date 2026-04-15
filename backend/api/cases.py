from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from core.database import get_db
from models.models import Case, Hearing, AuditLog
from services.priority_engine import compute_priority
from api.auth import get_current_user

router = APIRouter()

class CaseCreate(BaseModel):
    case_id_number: str
    primary_case_nature: str = "Civil"
    procedural_stage: str = "Pre-Trial"
    custody_status: str = "None"
    immediate_risk: str = "None"
    financial_stake: bool = False
    estimated_severity: str = "Low"
    petitioner: Optional[str] = ""
    respondent: Optional[str] = ""
    under_acts: Optional[str] = ""
    under_sections: Optional[str] = ""
    is_undertrial: bool = False
    days_in_custody: int = 0

def serialize_case(c: Case, role: str = "judge") -> dict:
    result = compute_priority(c)
    base = {
        "id": c.id,
        "case_id_number": c.cnr_number or c.id,
        "primary_case_nature": c.primary_case_nature,
        "procedural_stage": c.current_stage,
        "filing_date": c.filing_date.strftime("%d %b %Y"),
        "petitioner": c.petitioner or "—",
        "respondent": c.respondent or "—",
        "under_sections": c.under_sections or "—",
        "is_undertrial": c.is_undertrial,
        "score": result["priority_score"],
        "band": result["band"],
        "omega": result["omega_flag"],
        "aging_factor": result["aging_factor"],
        "vulnerability": result["vulnerability"],
        "stage_coeff": result["stage_coeff"],
        "friction_index": c.friction_index,
        "section_436a": result["section_436a"],
    }
    if role == "judge":
        base["explanation"] = result["judge_explanation"]
    else:
        base["explanation"] = result["citizen_summary"]
    return base

@router.get("")
def get_cases(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cases = db.query(Case).all()
    serialized = [serialize_case(c, user["role"]) for c in cases]
    serialized.sort(key=lambda x: x["score"], reverse=True)
    return serialized

@router.post("")
def create_case(data: CaseCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = Case(
        cnr_number=data.case_id_number,
        primary_case_nature=data.primary_case_nature,
        current_stage=data.procedural_stage,
        custody_status=data.custody_status,
        immediate_risk=data.immediate_risk,
        financial_stake=data.financial_stake,
        estimated_severity=data.estimated_severity,
        petitioner=data.petitioner,
        respondent=data.respondent,
        under_acts=data.under_acts,
        under_sections=data.under_sections,
        is_undertrial=data.is_undertrial,
        days_in_custody=data.days_in_custody,
        filing_date=datetime.utcnow(),
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return {"status": "success", "id": c.id, "cnr": c.cnr_number}

@router.put("/{case_id}/adjourn")
def adjourn_case(case_id: int, reason: str = "Not specified",
                 db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = db.query(Case).filter(Case.id == case_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Case not found")
    old_score = c.priority_score
    c.friction_index += 1
    c.updated_at = datetime.utcnow()
    result = compute_priority(c)
    c.priority_score = result["priority_score"]
    c.omega_flag = result["omega_flag"]
    db.add(AuditLog(
        case_id=case_id, action="adjournment",
        performed_by_role=user["role"],
        old_value=str(old_score),
        new_value=str(c.priority_score),
        detail={"reason": reason, "friction_index": c.friction_index}
    ))
    db.add(Hearing(
        case_id=case_id,
        purpose_of_hearing="Adjourned",
        adjournment_reason=reason,
        adjourned_by=user["role"],
        business_on_date=datetime.utcnow()
    ))
    db.commit()
    return {"status": "adjourned", "new_score": c.priority_score, "friction": c.friction_index, "omega": c.omega_flag}

@router.get("/analytics")
def get_analytics(db: Session = Depends(get_db), user=Depends(get_current_user)):
    cases = db.query(Case).all()
    if not cases:
        return {}
    scores = [compute_priority(c)["priority_score"] for c in cases]
    ages = [(datetime.utcnow().date() - c.filing_date.date()).days for c in cases]
    stage_dist = {}
    for c in cases:
        stage_dist[c.current_stage] = stage_dist.get(c.current_stage, 0) + 1
    return {
        "total_cases": len(cases),
        "total_priority_load": round(sum(scores), 1),
        "avg_age_days": round(sum(ages) / len(ages), 1),
        "omega_cases": len([c for c in cases if c.omega_flag]),
        "undertrial_cases": len([c for c in cases if c.is_undertrial]),
        "critical_cases": len([s for s in scores if s >= 200]),
        "cases_over_5_years": len([a for a in ages if a > 1825]),
        "stage_distribution": stage_dist,
        "oldest_case_days": max(ages),
    }