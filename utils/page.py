from core.models import Page


def _page_content(page: Page) -> dict[str, str]:
	return {
		"title": page.title,
		"description": page.description,
	}


def get_page_infos(page_path: str) -> dict[str, str]:
	page = Page.objects.filter(path=page_path).first()
	if page is None:
		return {}

	return {
		"seo_title": page.seo_title,
		"seo_description": page.seo_description,
		"seo_canonical_url": page.seo_canonical_url,
		"seo_og_title": page.seo_og_title,
		"seo_og_description": page.seo_og_description,
		"seo_og_type": page.seo_og_type,
		"seo_og_image": page.seo_og_image,
		"page": _page_content(page),
		"under_construction": page.under_construction,
	}


def get_pages_infos() -> dict[str, dict[str, str]]:
	return {
		page.path.replace("/", "_"): _page_content(page)
		for page in Page.objects.all()
	}
