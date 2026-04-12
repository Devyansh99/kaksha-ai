from src.pipeline.taxonomy_normalization import normalize_label


def test_normalize_label_maps_aliases_deterministically() -> None:
    alias = normalize_label("added denominators")
    assert alias["raw_label"] == "added denominators"
    assert alias["normalized_label"] == "Denominator addition"
    assert alias["taxonomy_group"] == "Fractions"
    assert alias["normalization_reason"] == "alias_match"

    unknown = normalize_label("completely unknown misconception")
    assert unknown["normalized_label"] == "Uncategorized"
    assert unknown["taxonomy_group"] == "Uncategorized"
    assert unknown["normalization_reason"] == "no_taxonomy_match"
