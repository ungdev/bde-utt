from django.db import models
from members.models import Team
from utils.models import picture_upload_to


class News(models.Model):
    def _news_picture_upload_to(instance, filename):
        return picture_upload_to("news")

    title: models.CharField = models.CharField(max_length=200)
    description: models.TextField = models.TextField()
    start_date: models.DateTimeField = models.DateTimeField()
    end_date: models.DateTimeField = models.DateTimeField()
    picture: models.ImageField = models.ImageField(
        upload_to=_news_picture_upload_to, blank=True, null=True
    )
    url: models.URLField = models.URLField(blank=True, null=True)
    teams: models.ManyToManyField = models.ManyToManyField(
        Team,
        blank=True,
        related_name="news_teams",
    )
    enable: models.BooleanField = models.BooleanField(
        default=False, help_text="Afficher/Cacher l'actualité"
    )

    def __str__(self):
        return self.title

    @property
    def teams_names(self):
        return ", ".join(team.name for team in self.teams.all())

    @property
    def period_string(self):
        if self.start_date.date() == self.end_date.date():
            return f"{self.start_date.strftime('%d/%m/%Y %H:%M')} - {self.end_date.strftime('%H:%M')}"
        else:
            return f"{self.start_date.strftime('%d/%m/%Y %H:%M')} - {self.end_date.strftime('%d/%m/%Y %H:%M')}"

    @property
    def picture_url(self):
        return f"/uploads/{self.picture}"


class Partner(models.Model):

    def _partner_picture_upload_to(instance, filename):
        return picture_upload_to("partners")

    name: models.CharField = models.CharField(max_length=200)
    description: models.TextField = models.TextField(blank=True)
    icon: models.ImageField = models.ImageField(upload_to=_partner_picture_upload_to)
    url: models.URLField = models.URLField(blank=True, null=True)
    enable: models.BooleanField = models.BooleanField(
        default=False, help_text="Afficher/Cacher le partenaire"
    )
    order: models.PositiveIntegerField = models.PositiveIntegerField(
        default=0, help_text="Ordre d'affichage"
    )

    def __str__(self):
        return self.name

    @property
    def icon_url(self):
        return f"/uploads/{self.icon}"

    class Meta:
        ordering = ["order"]
