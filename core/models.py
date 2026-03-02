from django.db import models


class Setting(models.Model):
    objects: models.Manager["Setting"] = models.Manager()

    key = models.CharField(max_length=200, unique=True)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.key} - {self.value}"
