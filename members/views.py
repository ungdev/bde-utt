from django.shortcuts import render
from django.contrib.auth.models import User
from .models import RoleCode, Team, TeamTemplate, UserTeam, UserTeamTemplate
from utils.views import common_data
from typing import TypedDict, cast


class TeamWithMembersTemplate(TeamTemplate):
    members: list[UserTeamTemplate]


def board(request):
    members_qs = (
        UserTeam.objects.select_related("user")
        .filter(team__name="Bureau")
        .only("user__id", "user__first_name", "user__last_name", "role")
    )
    role_order: list[RoleCode] = [role for role, _ in UserTeam.ROLES]
    members: list[UserTeam] = sorted(
        members_qs,
        key=lambda m: (
            role_order.index(m.role) if m.role in role_order else len(role_order),
            cast(User, m.user).last_name,
        ),
    )

    other_teams = (
        UserTeam.objects.exclude(team__name="Bureau")
        .filter(user__in=[member.user for member in members])
        .only("team__name")
    )

    return render(
        request,
        "board/main.html",
        {
            **common_data(
                request,
                seo={
                    "title": "BDE UTT | Bureau",
                    "description": "Decouvrez les membres du bureau du BDE UTT et leurs roles.",
                },
            ),
            "members": [
                {
                    **member.to_template(),
                    "other_teams": other_teams.filter(
                        user__id=cast(User, member.user).pk
                    ),
                }
                for member in members
            ],
        },
    )


def members(request):

    teams = Team.objects.exclude(name="Bureau")
    users_team = UserTeam.objects.exclude(team__name="Bureau").only(
        "user", "role", "team"
    )

    role_order: list[RoleCode] = [role for role, _ in UserTeam.ROLES]

    teams_with_members: list[TeamWithMembersTemplate] = sorted(
        [
            {
                **team.to_template(),
                "members": sorted(
                    [
                        ut.to_template()
                        for ut in users_team
                        if cast(Team, ut.team).pk == team.pk
                    ],
                    key=lambda m: (
                        role_order.index(m["role"]),
                        m["last_name"].lower(),
                    ),
                ),
            }
            for team in teams
        ],
        key=lambda t: t["name"].lower(),
    )

    return render(
        request,
        "members/main.html",
        {
            **common_data(
                request,
                seo={
                    "title": "BDE UTT | Commissions",
                    "description": "Retrouvez les commissions du BDE UTT et les membres qui les composent.",
                },
            ),
            "teams": teams_with_members,
        },
    )
