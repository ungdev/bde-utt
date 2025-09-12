from django.shortcuts import render
from .models import MemberProfile
from utils.views import common_data


def board(request):
    members = MemberProfile.objects.filter(team__name="Bureau").select_related("user")
    return render(
        request,
        "board.html",
        {
            **common_data(),
            "members": members,
        },
    )


def members(request):
    members = MemberProfile.objects.select_related("user").all()
    return render(
        request,
        "members.html",
        {
            **common_data(),
            "members": members,
        },
    )
