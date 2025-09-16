import os, requests

BASE_URL = os.getenv("OFF_BASE_URL", "https://world.openfoodfacts.org")
PRODUCT_PATH = "/api/v2/product/{barcode}.json"
TIMEOUT = float(os.getenv("OFF_TIMEOUT", "7"))
USER_AGENT = os.getenv("OFF_USER_AGENT", "Enviralyze (enviralyze@enviralyze.com)")

DEFAULT_FIELDS = ",".join([
    "code",
    "product_name",
    "brands",
    "categories",
    "image_url",
    "labels_tags",
    "nutriscore_grade",
    "ecoscore_grade",
    "ecoscore_score",
    "ecoscore_data",
    "last_modified_t",
])

def fetch_off_product(barcode: str, fields: str = DEFAULT_FIELDS) -> dict | None:
    url = f"{BASE_URL}{PRODUCT_PATH.format(barcode=barcode)}"
    r = requests.get(
        url,
        params={"fields": fields},
        headers={"User-Agent": USER_AGENT},
        timeout=TIMEOUT,
    )
    r.raise_for_status()
    data = r.json()
    if data.get("status") != 1:
        return None
    return data["product"]