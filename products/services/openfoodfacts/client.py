import os, requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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

_session = requests.Session()
_retry = Retry(
    total=3,
    backoff_factor=0.4,
    status_forcelist=(429, 500, 502, 503, 504),
    allowed_methods=frozenset(["GET"]),
    raise_on_status=False,
)
_session.mount("https://", HTTPAdapter(max_retries=_retry))
_session.headers.update({"User-Agent": USER_AGENT})

def fetch_off_product(
    barcode: str,
    *,
    fields: str = DEFAULT_FIELDS,
    if_none_match: str | None = None,
    if_modified_since_httpdate: str | None = None,
):
    url = f"{BASE_URL}{PRODUCT_PATH.format(barcode=barcode)}"

    headers = {}
    if if_none_match:
        headers["If-None-Match"] = if_none_match
    if if_modified_since_httpdate:
        headers["If-Modified-Since"] = if_modified_since_httpdate

    r = _session.get(
        url,
        params={"fields": fields},
        headers=headers,
        timeout=TIMEOUT,
    )

    if r.status_code == 304:
        return 304, r.headers, None

    r.raise_for_status()
    data = r.json()
    if data.get("status") != 1:
        return 200, r.headers, None
    return 200, r.headers, data["product"]