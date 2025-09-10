from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile
import re, secrets, imghdr, requests
from django.core.files.base import ContentFile
from allauth.account.signals import user_signed_up, user_logged_in
from allauth.socialaccount.signals import social_account_added
from allauth.socialaccount.models import SocialAccount

try:
    from PIL import Image
    from io import BytesIO
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

MAX_BYTES = 5 * 1024 * 1024
TIMEOUT = 7

def _normalize_google_photo_url(url: str) -> str | None:
    if not url:
        return None
    if "=s" in url:
        return re.sub(r"=s\d+(-c)?$", "=s512-c", url)
    if url.endswith("/"):
        return url + "=s512-c"
    return url + ("=s512-c" if ("=" not in url and "?" not in url) else "")

def _download_image(url: str) -> tuple[bytes | None, str | None]:
    try:
        headers = {"User-Agent": "enviralyze-avatar-fetcher/1.0"}
        with requests.get(url, headers=headers, stream=True, timeout=TIMEOUT) as r:
            r.raise_for_status()
            ctype = r.headers.get("Content-Type", "").lower()
            total, parts = 0, []
            for chunk in r.iter_content(64 * 1024):
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_BYTES:
                    return None, None
                parts.append(chunk)
        return b"".join(parts), ctype
    except Exception:
        return None, None

def _ext_from_content_type(ctype: str | None) -> str | None:
    if not ctype:
        return None
    if "jpeg" in ctype: return "jpg"
    if "png"  in ctype: return "png"
    if "webp" in ctype: return "webp"
    if "gif"  in ctype: return "gif"
    return None

def _guess_ext(raw: bytes, ctype: str | None) -> str:
    ext = _ext_from_content_type(ctype)
    if not ext:
        kind = imghdr.what(None, raw)
        ext = {"jpeg": "jpg"}.get(kind, kind)
    return ext or "bin"

def _convert_webp_to_jpg(raw: bytes) -> tuple[bytes, str]:
    if not PIL_AVAILABLE:
        return raw, "webp"
    try:
        im = Image.open(BytesIO(raw)).convert("RGB")
        out = BytesIO()
        im.save(out, format="JPEG", quality=92, optimize=True)
        return out.getvalue(), "jpg"
    except Exception:
        return raw, "webp"

def _save_avatar(user, raw: bytes, ext: str):
    if not raw:
        return
    if ext == "webp":
        raw, ext = _convert_webp_to_jpg(raw)
    if ext not in {"jpg", "jpeg", "png", "gif"}:
        return
    filename = f"google_{user.pk}_{secrets.token_hex(6)}.{ext}"
    user.profile.avatar.save(filename, ContentFile(raw), save=True)

def _maybe_pull_google_avatar(user, sociallogin=None):
    if getattr(user.profile, "avatar", None) and user.profile.avatar:
        return
    account = getattr(sociallogin, "account", None) if sociallogin else None
    if account is None:
        account = SocialAccount.objects.filter(user=user, provider="google").first()
    if not account or account.provider != "google":
        return
    picture_url = (account.extra_data or {}).get("picture")
    picture_url = _normalize_google_photo_url(picture_url)
    if not picture_url:
        return
    raw, ctype = _download_image(picture_url)
    if not raw:
        return
    ext = _guess_ext(raw, ctype)
    _save_avatar(user, raw, ext)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(user_signed_up)
def ensure_profile_on_signed_up(request, user, **kwargs):
    Profile.objects.get_or_create(user=user)
    _maybe_pull_google_avatar(user)

@receiver(user_logged_in)
def ensure_profile_on_logged_in(request, user, **kwargs):
    Profile.objects.get_or_create(user=user)
    if not getattr(user.profile, "avatar", None) or not user.profile.avatar:
        _maybe_pull_google_avatar(user)


@receiver(social_account_added)
def ensure_profile_on_social_added(request, sociallogin, **kwargs):
    user = sociallogin.user
    Profile.objects.get_or_create(user=user)
    _maybe_pull_google_avatar(user, sociallogin=sociallogin)