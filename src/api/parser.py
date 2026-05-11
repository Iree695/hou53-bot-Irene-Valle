import re
from typing import Any


NEIGHBORHOODS = [
    "Blmngtn",
    "Blueste",
    "BrDale",
    "BrkSide",
    "ClearCr",
    "CollgCr",
    "Crawfor",
    "Edwards",
    "Gilbert",
    "IDOTRR",
    "MeadowV",
    "Mitchel",
    "NAmes",
    "NoRidge",
    "NPkVill",
    "NridgHt",
    "NWAmes",
    "OldTown",
    "SWISU",
    "Sawyer",
    "SawyerW",
    "Somerst",
    "StoneBr",
    "Timber",
    "Veenker",
]

QUALITY_KEYWORDS = {
    9: ["luxury", "premium", "high-end", "excellent"],
    7: ["good", "renovated", "modern", "updated"],
    5: ["average", "standard", "typical"],
    3: ["fair", "basic", "simple"],
    2: ["poor", "old", "dated"],
}

HOUSE_STYLE_PATTERNS = {
    "1Story": [r"\bone[-\s]?story\b", r"\bsingle[-\s]?story\b"],
    "2Story": [r"\btwo[-\s]?story\b", r"\b2[-\s]?story\b"],
    "1.5Fin": [r"\bone and a half story\b", r"\b1\.5 story\b"],
    "SLvl": [r"\bsplit[-\s]?level\b"],
    "SFoyer": [r"\bsplit[-\s]?foyer\b"],
}


def _extract_int(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text)
    if not match:
        return None
    return int(match.group(1).replace(",", ""))


def _extract_float(pattern: str, text: str) -> float | None:
    match = re.search(pattern, text)
    if not match:
        return None
    return float(match.group(1).replace(",", ""))


def _extract_quality(text: str) -> int | None:
    for score, keywords in QUALITY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return score
    return None


def _extract_house_style(text: str) -> str | None:
    for style, patterns in HOUSE_STYLE_PATTERNS.items():
        if any(re.search(pattern, text) for pattern in patterns):
            return style
    return None


def _extract_neighborhood(text: str) -> str | None:
    normalized_text = text.lower()
    for neighborhood in NEIGHBORHOODS:
        if neighborhood.lower() in normalized_text:
            return neighborhood
    return None


def parse_house_description(description: str) -> dict[str, Any]:
    text = description.lower()
    features: dict[str, Any] = {}

    bedrooms = _extract_int(r"(\d+)\s*-?\s*bed(?:room)?s?", text)
    if bedrooms is not None:
        features["BedroomAbvGr"] = bedrooms

    bathrooms = _extract_int(r"(\d+)\s*-?\s*bath(?:room)?s?", text)
    if bathrooms is not None:
        features["FullBath"] = bathrooms

    area = _extract_float(r"(\d[\d,]*)\s*(?:sq\s*ft|square feet)", text)
    if area is not None:
        features["GrLivArea"] = area

    lot_area = _extract_float(r"lot of\s*(\d[\d,]*)\s*(?:sq\s*ft|square feet)", text)
    if lot_area is not None:
        features["LotArea"] = int(lot_area)

    garage_cars = _extract_int(r"(\d+)\s*-?\s*car garage", text)
    if garage_cars is not None:
        features["GarageCars"] = garage_cars

    year_built = _extract_int(r"(?:built in|year built)\s*(\d{4})", text)
    if year_built is not None:
        features["YearBuilt"] = year_built

    overall_quality = _extract_quality(text)
    if overall_quality is not None:
        features["OverallQual"] = overall_quality

    house_style = _extract_house_style(text)
    if house_style is not None:
        features["HouseStyle"] = house_style

    neighborhood = _extract_neighborhood(text)
    if neighborhood is not None:
        features["Neighborhood"] = neighborhood

    if "central air" in text or "air conditioning" in text:
        features["CentralAir"] = "Y"

    if "fireplace" in text:
        features["Fireplaces"] = 1

    if "paved driveway" in text:
        features["PavedDrive"] = "Y"

    if "gabled roof" in text or "gable roof" in text:
        features["RoofStyle"] = "Gable"

    if "hip roof" in text:
        features["RoofStyle"] = "Hip"

    return features
