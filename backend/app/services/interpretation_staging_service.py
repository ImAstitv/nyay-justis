# Thresholds are intentionally conservative to avoid silent misclassification

from typing import Dict, Any
from datetime import datetime


# Confidence thresholds per field
CONFIDENCE_THRESHOLDS = {
    "case_nature": 0.85,
    "procedural_stage": 0.80,
    "custody_status": 0.75,
    "property_livelihood_risk": 0.75,
    "severity_band": 0.65,
    "petitioner_age_band": 0.65,
    "case_complexity": 0.65,
}


class StagingDecision:
    """
    Represents the result of confidence gating.
    """

    def __init__(self, status: str, failed_fields: Dict[str, float]):
        self.status = status  # auto_approved | needs_review
        self.failed_fields = failed_fields
        self.timestamp = datetime.utcnow()


class InterpretationStagingService:
    """
    Handles confidence gating and prepares data for staging.
    """

    @staticmethod
    def evaluate(interpreted_fields: Dict[str, Any]) -> StagingDecision:
        """
        Evaluates interpretation confidence and determines whether
        the case can be auto-approved or requires human review.
        """

        failed = {}

        for field, result in interpreted_fields.items():
            threshold = CONFIDENCE_THRESHOLDS.get(field, 1.0)
            if result.confidence < threshold:
                failed[field] = result.confidence

        if failed:
            return StagingDecision(
                status="needs_review",
                failed_fields=failed
            )

        return StagingDecision(
            status="auto_approved",
            failed_fields={}
        )