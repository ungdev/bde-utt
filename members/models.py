from django.db import models
from django.contrib.auth.models import User
from utils.models import picture_upload_to


class Team(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    description: models.TextField = models.TextField(blank=True)

    def __str__(self):
        return self.name


class MemberProfile(models.Model):

    def _members_picture_upload_to(instance, filename):
        return picture_upload_to("members")

    ROLES = [
        ("PRESIDENT", "Président"),
        ("VICE_PRESIDENT", "Vice-Président"),
        ("SECRETARY", "Secrétaire"),
        ("TREASURER", "Trésorier"),
        ("MANAGER", "Responsable"),
        ("MEMBER", "Membre"),
    ]

    user: models.OneToOneField[User] = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    role: models.CharField = models.CharField(
        max_length=20, choices=ROLES, default="MEMBER"
    )
    team: models.ForeignKey[Team] = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True
    )
    picture: models.ImageField = models.ImageField(
        upload_to=_members_picture_upload_to, blank=True, null=True
    )

    @property
    def role_display(self):
        return dict(self.ROLES).get(self.role, "Unknown")

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} ({self.role_display})"
