from django.shortcuts import render
from .models import Team, UserTeam
from utils.views import common_data


def board(request):
    members = (
        UserTeam.objects.select_related("user")
        .filter(team__name="Bureau")
        .only("user__id", "user__first_name", "user__last_name", "role")
    )
    role_order = UserTeam.ROLES
    members = sorted(
        members,
        key=lambda m: (
            role_order.index(m.role) if m.role in role_order else len(role_order)
        ),
    )

    other_teams = (
        UserTeam.objects.exclude(team__name="Bureau")
        .filter(user__in=[member.user for member in members])
        .only("team__name")
    )

    return render(
        request,
        "board.html",
        {
            **common_data(),
            "members": [
                {
                    **member.to_template(),
                    "other_teams": other_teams.filter(user__id=member.user.pk),
                }
                for member in members
            ],
        },
    )


def members(request):

    teams = Team.objects.exclude(name="Bureau")
    users_team = UserTeam.objects.exclude(team__name="Bureau").only("user", "role")

    teams_with_members = [
        {
            **team.to_template(),
            "members": [ut.to_template() for ut in users_team if ut.team.pk == team.pk],
        }
        for team in teams
    ]

    return render(
        request,
        "members.html",
        {
            **common_data(),
            "teams": teams_with_members,
        },
    )
