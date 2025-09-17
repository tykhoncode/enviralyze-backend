from products.models import Product
from .client import fetch_off_product, DEFAULT_FIELDS
from .mapper import to_product_fields
from datetime import timedelta, datetime, timezone as py_tz
from email.utils import format_datetime as httpdate_format, parsedate_to_datetime
from django.utils import timezone
from django.db import transaction

STALE_DAYS = 7

def _to_httpdate(dt: datetime | None) -> str | None:
    if not dt:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=py_tz.utc)
    else:
        dt = dt.astimezone(py_tz.utc)
    return httpdate_format(dt)

def _from_httpdate(header_value: str | None) -> datetime | None:
    if not header_value:
        return None
    try:
        return parsedate_to_datetime(header_value).astimezone(py_tz.utc)
    except Exception:
        return None

def _is_stale(prod: Product) -> bool:
    if not prod.last_checked_at:
        return True
    return prod.last_checked_at <= timezone.now() - timedelta(days=STALE_DAYS)

@transaction.atomic
def _upsert_from_off(off: dict, *, etag: str | None, last_modified_hdr: str | None) -> Product:

    mapped = to_product_fields(off)
    if not mapped.get("off_last_modified_t"):
        mapped["off_last_modified_t"] = _from_httpdate(last_modified_hdr)

    prod, _created = Product.objects.update_or_create(
        barcode=mapped["barcode"],
        defaults={
            "name": mapped.get("name"),
            "brand": mapped.get("brand"),
            "category": "Food & Drinks",
            "image_url": mapped.get("image_url"),
            "sustainability_data": mapped.get("sustainability_data"),
            "source": "openfoodfacts",
            "off_last_modified_t": mapped.get("off_last_modified_t"),
            "off_etag": etag,
        },
    )
    prod.last_synced_at = timezone.now()
    prod.last_checked_at = timezone.now()
    prod.save(update_fields=[
        "last_synced_at", "off_last_modified_t", "off_etag", "last_checked_at",
        "name", "brand", "category", "image_url", "sustainability_data", "source"
    ])
    return prod

def get_or_update_if_needed(barcode: str, *, force: bool = False) -> Product | None:
    prod = Product.objects.filter(barcode=barcode).first()

    if not prod:
        status, headers, off = fetch_off_product(barcode, fields=DEFAULT_FIELDS)
        if not off:
            return None
        etag = headers.get("ETag")
        last_mod_hdr = headers.get("Last-Modified")
        return _upsert_from_off(off, etag=etag, last_modified_hdr=last_mod_hdr)

    if not force and not _is_stale(prod):
        return prod

    if_none_match = prod.off_etag
    if_modified_since = _to_httpdate(prod.off_last_modified_t)

    status, headers, off = fetch_off_product(
        barcode,
        fields=DEFAULT_FIELDS,
        if_none_match=if_none_match,
        if_modified_since_httpdate=if_modified_since
    )

    if status == 304:
        prod.last_checked_at = timezone.now()
        prod.save(update_fields=["last_checked_at"])
        return prod

    if status == 200 and off is None:
        prod.last_checked_at = timezone.now()
        prod.save(update_fields=["last_checked_at"])
        return prod

    if status == 200 and off:
        etag = headers.get("ETag")
        last_mod_hdr = headers.get("Last-Modified")
        return _upsert_from_off(off, etag=etag, last_modified_hdr=last_mod_hdr)

    return prod