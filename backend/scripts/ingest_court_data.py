from __future__ import annotations

from pathlib import Path
import argparse
import csv
import json
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.database import SessionLocal
from models.models import Case


def _read_rows(path: Path) -> list[dict]:
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise SystemExit("JSON input must be an array of case records.")
        return [row for row in data if isinstance(row, dict)]

    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    raise SystemExit("Supported input formats are .csv and .json")


def _as_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() in {"1", "true", "yes", "y"}


def _as_int(value, default: int = 0) -> int:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def _pick(row: dict, *keys: str, default=""):
    for key in keys:
        if key in row and row[key] not in (None, ""):
            return row[key]
    return default


def ingest_rows(rows: list[dict], replace_existing: bool = False) -> tuple[int, int]:
    db = SessionLocal()
    created = 0
    updated = 0
    try:
        for row in rows:
            cnr_number = str(_pick(row, "case_id_number", "cnr_number", "cnr", default="")).strip()
            if not cnr_number:
                continue

            case = db.query(Case).filter(Case.cnr_number == cnr_number).first()
            if case is None:
                case = Case(cnr_number=cnr_number)
                db.add(case)
                created += 1
            elif not replace_existing:
                continue
            else:
                updated += 1

            case.primary_case_nature = str(_pick(row, "primary_case_nature", "case_type", default="Civil")).strip() or "Civil"
            case.current_stage = str(_pick(row, "procedural_stage", "current_stage", default="Pre-Trial")).strip() or "Pre-Trial"
            case.petitioner = str(_pick(row, "petitioner", "party_a", default="")).strip()
            case.respondent = str(_pick(row, "respondent", "party_b", default="")).strip()
            case.under_acts = str(_pick(row, "under_acts", "acts", default="")).strip()
            case.under_sections = str(_pick(row, "under_sections", "sections", default="")).strip()
            case.custody_status = str(_pick(row, "custody_status", default="None")).strip() or "None"
            case.immediate_risk = str(_pick(row, "immediate_risk", default="None")).strip() or "None"
            case.estimated_severity = str(_pick(row, "estimated_severity", default="Low")).strip() or "Low"
            case.financial_stake = _as_bool(_pick(row, "financial_stake", default=False))
            case.is_undertrial = _as_bool(_pick(row, "is_undertrial", default=False))
            case.days_in_custody = _as_int(_pick(row, "days_in_custody", default=0))
            case.status = str(_pick(row, "status", default="Active")).strip() or "Active"

        db.commit()
        return created, updated
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Import staged court data from CSV or JSON.")
    parser.add_argument("--file", required=True, help="Path to a CSV or JSON file containing case rows.")
    parser.add_argument("--replace-existing", action="store_true", help="Update existing cases with matching CNR/case IDs.")
    args = parser.parse_args()

    input_path = Path(args.file).resolve()
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    rows = _read_rows(input_path)
    created, updated = ingest_rows(rows, replace_existing=args.replace_existing)
    print(f"Court data import complete. Created: {created}, Updated: {updated}, Rows read: {len(rows)}")


if __name__ == "__main__":
    main()
