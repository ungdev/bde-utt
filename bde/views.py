from django.shortcuts import redirect, render
from django.contrib.auth import logout
from bde.env import EnvConfig
from utils.views import common_data

env = EnvConfig()


def admin_redirect_view(request):
    return redirect(f"/{env.ADMIN_URL}")


def admin_logout(request):
    if request.user.is_authenticated:
        logout(request)
    next_url = request.GET.get("next", "/")
    return redirect(next_url)


def legal(request):
    return render(
        request,
        "legal.html",
        {**common_data()},
    )
