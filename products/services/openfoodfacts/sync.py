from products.models import Product
from .client import fetch_off_product, DEFAULT_FIELDS
from .mapper import to_product_fields

def upsert_from_off(off: dict) -> Product:
    fields = to_product_fields(off)
    prod, _created = Product.objects.update_or_create(
        barcode=fields["barcode"],
        defaults={
            "name": fields["name"],
            "brand": fields["brand"],
            "category": "Food & Drinks",
            "image_url": fields["image_url"],
            "off_last_modified_t": fields["off_last_modified_t"],
            "sustainability_data": fields["sustainability_data"],
            "source": "off",
        },
    )
    prod.mark_synced(fields.get("off_last_modified_t"))
    prod.save(update_fields=[
        "last_synced_at", "off_last_modified_t", "name", "brand",
        "category", "image_url", "sustainability_data", "source"
    ])
    return prod

def sync_from_off(barcode: str) -> Product | None:
    off_product = fetch_off_product(barcode, fields=DEFAULT_FIELDS)
    if not off_product:
        return None
    return upsert_from_off(off_product)