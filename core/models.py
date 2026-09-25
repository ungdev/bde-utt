from django.db import models
from django.forms import Textarea


class Setting(models.Model):
    objects: models.Manager["Setting"] = models.Manager()

    key = models.CharField(max_length=200, unique=True)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.key} - {self.value}"

class Page(models.Model):
    objects: models.Manager["Page"] = models.Manager()

    path = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200, blank=True, help_text="Le titre de la page qui s'affiche en haut de la page.")
    description = models.TextField(blank=True, help_text="La description de la page qui s'affiche en haut de la page et dans les cartes d'aperçu.")
    under_construction = models.BooleanField(default=False, help_text="Cochez cette case si la page est en construction. Cela affichera un message d'information aux visiteurs.")
    seo_title = models.CharField(max_length=200, blank=True, help_text="Le titre SEO de la page sert à améliorer le référencement et l'affichage dans les résultats de recherche.")
    seo_description = models.TextField(blank=True, help_text="La description SEO de la page sert à améliorer le référencement et l'affichage dans les résultats de recherche.")
    seo_canonical_url = models.CharField(max_length=500, blank=True, help_text="Laisser vide pour utiliser l'URL canonique par défaut de la page.")
    seo_og_title = models.CharField(max_length=200, blank=True, help_text="Laisser vide pour utiliser le titre SEO.")
    seo_og_description = models.TextField(blank=True, help_text="Laisser vide pour utiliser la description SEO.")
    seo_og_type = models.CharField(max_length=50, blank=True, default="website", help_text="Type d'objet Open Graph (ex: 'website', 'article', etc.).")
    seo_og_image = models.CharField(max_length=500, blank=True, help_text="URL de l'image Open Graph. Laisser vide pour utiliser l'image par défaut du site.")

    def __str__(self):
        return f"{self.path}"

class TextArea(models.Model):
    objects: models.Manager["Textarea"] = models.Manager()
    formfield_for_dbfield = Textarea

    key = models.CharField(max_length=200)
    content = models.TextField(help_text="Le contenu de la zone de texte. Vous pouvez utiliser du HTML pour formater le texte.")

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="textareas")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["page", "key"],
                name="unique_textarea_page_key",
            ),
        ]

    def __str__(self):
        return f"{self.page} - {self.key}"
