from showcase.models import Partner
from datetime import datetime
import json
from typing import Any
from django.http import HttpRequest
from bde.settings import DEFAULT_SEO_TITLE, DEFAULT_SEO_DESCRIPTION, DEFAULT_SEO_IMAGE


def _absolute_url(request: HttpRequest | None, path: str) -> str:
    if request is None:
        return path
    return request.build_absolute_uri(path)


def build_seo_data(
    request: HttpRequest | None = None,
    seo: dict[str, Any] | None = None,
) -> dict[str, str]:
    seo = seo or {}

    title = str(seo.get("title") or DEFAULT_SEO_TITLE)
    description = str(seo.get("description") or DEFAULT_SEO_DESCRIPTION)
    canonical_url = str(seo.get("canonical_url") or _absolute_url(request, ""))
    og_title = str(seo.get("og_title") or title)
    og_description = str(seo.get("og_description") or description)
    og_type = str(seo.get("og_type") or "website")
    og_image = str(seo.get("og_image") or _absolute_url(request, DEFAULT_SEO_IMAGE))

    return {
        "seo_title": title,
        "seo_description": description,
        "seo_canonical_url": canonical_url,
        "seo_og_title": og_title,
        "seo_og_description": og_description,
        "seo_og_type": og_type,
        "seo_og_url": canonical_url,
        "seo_og_image": og_image,
    }


def common_data(
    request: HttpRequest | None = None,
    seo: dict[str, Any] | None = None,
):

    partners_qs = Partner.objects.filter(enable=True).order_by("order")
    partners_list = [
        {
            "name": p.name,
            "description": p.description,
            "icon_url": p.icon_url,
            "url": p.url,
        }
        for p in partners_qs
    ]

    return {
        "partners_qs": partners_qs,
        "partners_json": json.dumps(partners_list),
        "current_year": datetime.now().year,
        **build_seo_data(request, seo),
    }
