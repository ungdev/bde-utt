from core.models import TextArea

class Textareas:

	@classmethod
	def for_page(cls, page_path: str) -> dict[str, str]:
		return {
			textarea.key: textarea.content
			for textarea in TextArea.objects.filter(page__path=page_path)
		}

	@classmethod
	def for_page_and_key(cls, page_path: str, key: str) -> str | None:
		textarea = TextArea.objects.filter(page__path=page_path, key=key).first()
		return textarea.content if textarea else None


def get_textareas(page_path: str) -> dict[str, str]:
	return Textareas.for_page(page_path)

def get_textarea(page_path: str, key: str) -> str | None:
	return Textareas.for_page_and_key(page_path, key)
