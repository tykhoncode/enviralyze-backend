from datetime import datetime, timezone as py_tz

def to_product_fields(off: dict) -> dict:
    brand = (off.get("brands") or "").split(",")[0].strip() or None

    lm = off.get("last_modified_t")
    off_last_modified = datetime.fromtimestamp(lm, tz=py_tz.utc) if lm else None

    eco_data = off.get("ecoscore_data") or {}
    packaging_score = eco_data.get("adjustments", {}).get("packaging", {}).get("score")
    agribalyse = eco_data.get("agribalyse", {})
    agribalyse_score = agribalyse.get("score")
    co2_total = agribalyse.get("co2_total")

    labels = off.get("labels_tags", []) or []
    certs = {
        "organic": "organic" in labels or "eu-organic" in labels or "bio" in labels,
        "fair_trade": "fair-trade" in labels,
        "fsc_packaging": "fsc" in labels or "fsc-packaging" in labels,
        "carbon_neutral": "carbon-neutral" in labels,
    }

    sustainability = {
        "ecoscore_score": off.get("ecoscore_score"),
        "packaging_score": packaging_score,
        "agribalyse_score": agribalyse_score,
        "co2_total_emissions": co2_total,
        "certifications": certs,
    }

    return {
        "barcode": off.get("code"),
        "name": off.get("product_name"),
        "brand": brand,
        "image_url": off.get("image_url"),
        "off_last_modified_t": off_last_modified,
        "sustainability_data": sustainability,
    }