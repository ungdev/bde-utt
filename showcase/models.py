from django.db import models
from members.models import Team
from utils.models import picture_upload_to


class Partner(models.Model):

    def _partner_picture_upload_to(instance, filename):
        return picture_upload_to("partners")

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    icon = models.ImageField(upload_to=_partner_picture_upload_to)
    url = models.URLField(blank=True, null=True)
    enable = models.BooleanField(
        default=False, help_text="Afficher/Cacher le partenaire"
    )
    order = models.PositiveIntegerField(
        default=0, help_text="Ordre d'affichage (0 = premier)"
    )

    def __str__(self):
        return str(self.name)

    @property
    def icon_url(self):
        return f"/uploads/{self.icon}"

    class Meta:
        ordering = ["order"]
