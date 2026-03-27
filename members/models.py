from __future__ import annotations

from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from utils.models import picture_upload_to
from typing import Literal, TypedDict, cast


RoleCode = Literal[
    "PRESIDENT",
    "VICE_PRESIDENT",
    "SECRETARY",
    "TREASURER",
    "VICE_TREASURER",
    "MANAGER",
    "MEMBER",
]


class TeamTemplate(TypedDict):
    name: str
    description: str


class UserTeamTemplate(TypedDict):
    first_name: str
    last_name: str
    role: RoleCode
    role_display: str
    role_suffix: str
    profile: "UserProfile | None"


class Team(models.Model):
    name: models.CharField = models.CharField(max_length=100)
    description: models.TextField = models.TextField(blank=True)

    def to_template(self) -> TeamTemplate:
        return {"name": self.name, "description": self.description}

    def __str__(self) -> str:
        return cast(str, self.name)


class UserProfile(models.Model):
    def _members_picture_upload_to(instance, _) -> str:
        return picture_upload_to("members")

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture: models.ImageField = models.ImageField(
        upload_to=_members_picture_upload_to, blank=True, null=True
    )

    description: models.TextField = models.TextField(blank=True)
    feminine_role: models.BooleanField = models.BooleanField(default=False)

    @property
    def picture_url(self) -> str:
        return f"/uploads/{self.picture}"

    def __str__(self) -> str:
        user: User = self.user
        return f"{user.first_name} {user.last_name} ({self.picture})"


class UserTeam(models.Model):

    FEMINIZABLE_ROLES: set[RoleCode] = {
        "PRESIDENT",
        "VICE_PRESIDENT",
        "TREASURER",
        "VICE_TREASURER",
    }

    ROLES: list[tuple[RoleCode, str]] = [
        ("PRESIDENT", "Président"),
        ("TREASURER", "Trésorier"),
        ("VICE_TREASURER", "Vice-Trésorier"),
        ("VICE_PRESIDENT", "Vice-Président"),
        ("SECRETARY", "Secrétaire"),
        ("MANAGER", "Responsable"),
        ("MEMBER", "Membre"),
    ]

    user: models.ForeignKey[User] = models.ForeignKey(User, on_delete=models.CASCADE)

    role: models.CharField = models.CharField(
        max_length=20, choices=ROLES, default="MEMBER"
    )

    team: models.ForeignKey[Team] = models.ForeignKey(Team, on_delete=models.CASCADE)

    @property
    def role_display(self) -> str:
        return dict(self.ROLES).get(self.role, "Unknown")

    def role_suffix(self, profile: UserProfile | None) -> str:
        if profile and profile.feminine_role and self.role in self.FEMINIZABLE_ROLES:
            return "e"
        return ""

    def to_template(self) -> UserTeamTemplate:
        user = cast(User, self.user)
        profile = get_userProfile_from_userTeam(self)
        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": self.role,
            "role_display": self.role_display,
            "role_suffix": self.role_suffix(profile),
            "profile": profile,
        }

    def __str__(self) -> str:
        user = cast(User, self.user)
        team = cast(Team, self.team)
        first_name = user.first_name
        last_name = user.last_name
        team_name = team.name
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
