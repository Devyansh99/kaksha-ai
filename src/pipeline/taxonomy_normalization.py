from __future__ import annotations

from typing import Any

TAXONOMY_VERSION = "v1"

CANONICAL_LABELS: dict[str, str] = {
    "Denominator": "Fractions",
    "Denominator addition": "Fractions",
    "Structure": "Conceptual",
    "Reduction": "Fractions",
    "Sign error": "Arithmetic",
    "Order of operations": "Arithmetic",
    "Place value": "Number sense",
}

ALIAS_TO_CANONICAL: dict[str, str] = {
    "denominator error": "Denominator",
    "added denominators": "Denominator addition",
    "common denominator confusion": "Denominator",
    "structure confusion": "Structure",
    "simplification": "Reduction",
}

_LOWER_CANONICAL: dict[str, str] = {label.lower(): label for label in CANONICAL_LABELS}


def normalize_label(raw_label: str) -> dict[str, Any]:
    value = str(raw_label or "").strip()

    if value in CANONICAL_LABELS:
        canonical = value
        reason = "exact_canonical_match"
    else:
        lowered = value.lower()
        if lowered in _LOWER_CANONICAL:
            canonical = _LOWER_CANONICAL[lowered]
            reason = "canonical_casefold_match"
        elif lowered in ALIAS_TO_CANONICAL:
            canonical = ALIAS_TO_CANONICAL[lowered]
            reason = "alias_match"
        else:
            canonical = "Uncategorized"
            reason = "no_taxonomy_match"

    return {
        "raw_label": value,
        "normalized_label": canonical,
        "taxonomy_group": CANONICAL_LABELS.get(canonical, "Uncategorized"),
        "normalization_reason": reason,
        "taxonomy_version": TAXONOMY_VERSION,
    }
