from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.authz import require_case_owner, require_roles
from core.database import get_db
from models.models import Case, Hearing
from services.priority_engine import compute_priority

router = APIRouter()


@router.get("/search")
def search(q: str = "", db: Session = Depends(get_db), user=Depends(require_roles("citizen"))):
    q = q.strip()
    if not q:
        return []

    cases = db.query(Case).filter(Case.cnr_number == q).limit(1).all()

    results = []
    for c in cases:
        require_case_owner(c, user)
        result = compute_priority(c)
        hearings = db.query(Hearing).filter(Hearing.case_id == c.id).order_by(Hearing.created_at).all()
        timeline = [
            {
                "date": h.business_on_date.strftime("%d %b %Y") if h.business_on_date else "-",
                "event": h.purpose_of_hearing or "Hearing",
                "note": h.adjournment_reason or "",
            }
            for h in hearings
        ]
        results.append(
            {
                "id": c.id,
                "case_id_number": c.cnr_number,
                "primary_case_nature": c.primary_case_nature,
                "procedural_stage": c.current_stage,
                "status": c.status,
                "filing_date": c.filing_date.strftime("%d %b %Y"),
                "band": result["band"],
                "explanation": result["citizen_summary"],
                "timeline": timeline,
            }
        )
    return results
