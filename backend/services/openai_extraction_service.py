import base64
import json
from typing import Any

import requests

from core.config import settings


class OpenAIExtractionError(Exception):
    pass


OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses"

CASE_EXTRACTION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "fields": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "case_id_number": {"type": "string"},
                "primary_case_nature": {"type": "string"},
                "procedural_stage": {"type": "string"},
                "custody_status": {"type": "string"},
                "immediate_risk": {"type": "string"},
                "financial_stake": {"type": "boolean"},
                "estimated_severity": {"type": "string"},
                "petitioner": {"type": "string"},
                "respondent": {"type": "string"},
                "under_acts": {"type": "string"},
                "under_sections": {"type": "string"},
                "is_undertrial": {"type": "boolean"},
                "days_in_custody": {"type": "integer"},
            },
            "required": [
                "case_id_number",
                "primary_case_nature",
                "procedural_stage",
                "custody_status",
                "immediate_risk",
                "financial_stake",
                "estimated_severity",
                "petitioner",
                "respondent",
                "under_acts",
                "under_sections",
                "is_undertrial",
                "days_in_custody",
            ],
        },
        "confidence": {"type": "integer"},
        "fields_extracted": {"type": "integer"},
        "missing_fields": {"type": "array", "items": {"type": "string"}},
        "warnings": {"type": "array", "items": {"type": "string"}},
        "language": {"type": "string"},
        "summary": {"type": "string"},
    },
    "required": [
        "fields",
        "confidence",
        "fields_extracted",
        "missing_fields",
        "warnings",
        "language",
        "summary",
    ],
}

TRANSLATION_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "source_language": {"type": "string"},
        "target_language": {"type": "string"},
        "translated_text": {"type": "string"},
        "notes": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["source_language", "target_language", "translated_text", "notes"],
}


def _is_openai_configured() -> bool:
    return bool(settings.OPENAI_API_KEY and settings.OPENAI_EXTRACTION_MODEL)


def _headers() -> dict[str, str]:
    if not _is_openai_configured():
        raise OpenAIExtractionError("OpenAI document extraction is not configured")
    return {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }


def _post_responses_api(payload: dict[str, Any]) -> dict[str, Any]:
    try:
        response = requests.post(
            OPENAI_RESPONSES_URL,
            headers=_headers(),
            json=payload,
            timeout=settings.OPENAI_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise OpenAIExtractionError(f"OpenAI request failed: {exc}")


def _extract_output_text(response_json: dict[str, Any]) -> str:
    output_text = response_json.get("output_text")
    if output_text:
        return output_text.strip()

    output_items = response_json.get("output", [])
    for item in output_items:
        for content in item.get("content", []):
            if content.get("type") == "output_text" and content.get("text"):
                return content["text"].strip()

    raise OpenAIExtractionError("OpenAI response did not include output text")


def get_openai_extraction_health() -> dict[str, Any]:
    return {
        "configured": _is_openai_configured(),
        "model": settings.OPENAI_EXTRACTION_MODEL,
        "provider": "openai",
        "timeout_seconds": settings.OPENAI_TIMEOUT_SECONDS,
        "multilingual_enabled": settings.ENABLE_MULTILINGUAL_PIPELINE,
        "supported_document_languages": settings.SUPPORTED_DOCUMENT_LANGUAGES,
        "translation_target_language": settings.MULTILINGUAL_TARGET_LANGUAGE,
    }


def extract_document_text(file_bytes: bytes, content_type: str | None, filename: str | None) -> dict[str, Any]:
    encoded = base64.b64encode(file_bytes).decode("utf-8")
    document_name = filename or "uploaded_document"
    prompt = (
        "Read this legal document carefully. Extract the document text as faithfully as possible. "
        "Preserve line breaks where useful. Do not summarize. Return only the document text."
    )

    if content_type == "application/pdf":
        content = [
            {
                "type": "input_file",
                "filename": document_name,
                "file_data": encoded,
            },
            {"type": "input_text", "text": prompt},
        ]
    else:
        content = [
            {
                "type": "input_image",
                "image_url": f"data:{content_type or 'image/png'};base64,{encoded}",
                "detail": "high",
            },
            {"type": "input_text", "text": prompt},
        ]

    payload = {
        "model": settings.OPENAI_EXTRACTION_MODEL,
        "input": [{"role": "user", "content": content}],
    }
    response_json = _post_responses_api(payload)
    return {
        "text": _extract_output_text(response_json),
        "source": "openai_document_extraction",
        "provider": "openai",
        "model": settings.OPENAI_EXTRACTION_MODEL,
    }


def extract_case_fields_with_openai(text: str) -> dict[str, Any]:
    prompt = (
        "Extract case-filing fields from the provided court document text. "
        "The text may be in English, Hindi, or another Indian language. "
        "Preserve names exactly as written where possible. "
        "Normalize enum-like workflow fields to these English values only when inferable: "
        "primary_case_nature: Civil or Criminal; "
        "procedural_stage: Pre-Trial, Framing of Charges, Evidence, Arguments, Active Trial, Sentencing; "
        "custody_status: None, Remand, Bail Denied; "
        "immediate_risk: None, Flight Risk, Threat to Life, Loss of Livelihood; "
        "estimated_severity: Low, Medium, High. "
        "If a field is unknown, return an empty string, false, or 0 as appropriate. "
        "Return fields suitable for pre-filling a human review form."
    )
    payload = {
        "model": settings.OPENAI_EXTRACTION_MODEL,
        "input": [
            {
                "role": "system",
                "content": [{"type": "input_text", "text": prompt}],
            },
            {
                "role": "user",
                "content": [{"type": "input_text", "text": text}],
            },
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "case_extraction",
                "schema": CASE_EXTRACTION_SCHEMA,
                "strict": True,
            }
        },
    }
    response_json = _post_responses_api(payload)
    output_text = _extract_output_text(response_json)
    try:
        extracted = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise OpenAIExtractionError(f"OpenAI returned invalid JSON: {exc}")

    extracted["provider"] = "openai"
    extracted["model"] = settings.OPENAI_EXTRACTION_MODEL
    return extracted


def translate_legal_text(text: str, target_language: str | None = None) -> dict[str, Any]:
    desired_language = target_language or settings.MULTILINGUAL_TARGET_LANGUAGE
    prompt = (
        "Translate the provided legal text into the requested target language. "
        "Preserve names, case numbers, statute references, dates, and legal section references exactly. "
        "Do not omit material facts. If the text is already in the target language, return a faithful cleaned copy. "
        "Return JSON only."
    )
    payload = {
        "model": settings.OPENAI_EXTRACTION_MODEL,
        "input": [
            {
                "role": "system",
                "content": [{"type": "input_text", "text": prompt}],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": f"Target language: {desired_language}\n\nSource text:\n{text}",
                    }
                ],
            },
        ],
        "text": {
            "format": {
                "type": "json_schema",
                "name": "legal_translation",
                "schema": TRANSLATION_SCHEMA,
                "strict": True,
            }
        },
    }
    response_json = _post_responses_api(payload)
    output_text = _extract_output_text(response_json)
    try:
        translated = json.loads(output_text)
    except json.JSONDecodeError as exc:
        raise OpenAIExtractionError(f"OpenAI returned invalid translation JSON: {exc}")

    translated["provider"] = "openai"
    translated["model"] = settings.OPENAI_EXTRACTION_MODEL
    return translated
