from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from utils.models import picture_upload_to


class Team(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    description: models.TextField = models.TextField(blank=True)

    def to_template(self):
        return {"name": self.name, "description": self.description}

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    def _members_picture_upload_to(instance, filename):
        return picture_upload_to("members")

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture: models.ImageField = models.ImageField(
        upload_to=_members_picture_upload_to, blank=True, null=True
    )

    description: models.TextField = models.TextField(blank=True)

    @property
    def picture_url(self):
        return f"/uploads/{self.picture}"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.picture})"


class UserTeam(models.Model):

    ROLES = [
        ("PRESIDENT", "Président"),
        ("VICE_PRESIDENT", "Vice-Président"),
        ("SECRETARY", "Secrétaire"),
        ("TREASURER", "Trésorier"),
        ("MANAGER", "Responsable"),
        ("MEMBER", "Membre"),
    ]

    user: models.ForeignKey[User] = models.ForeignKey(User, on_delete=models.CASCADE)

    role: models.CharField = models.CharField(
        max_length=20, choices=ROLES, default="MEMBER"
    )

    team: models.ForeignKey[Team] = models.ForeignKey(Team, on_delete=models.CASCADE)

    @property
    def role_display(self):
        return dict(self.ROLES).get(self.role, "Unknown")

    def to_template(self):
        return {
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "role_display": self.role_display,
            "profile": get_userProfile_from_userTeam(self),
        }

    def __str__(self) -> str:
        first_name = getattr(self.user, "first_name", "")
        last_name = getattr(self.user, "last_name", "")
        team_name = getattr(self.team, "name", "")
        return f"{first_name} {last_name} ({team_name} - {self.role_display})"


def get_userProfile_from_userTeam(member: UserTeam) -> UserProfile | None:
    try:
        user = getattr(member, "user", None)
        if user is None:
            return None
        user_profile = UserProfile.objects.get(user__id=user.id)

        user_profile.description = mark_safe(
            user_profile.description.replace("\n", "<br>")
        )
        return user_profile
    except UserProfile.DoesNotExist:
        return None
