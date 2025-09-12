from django.shortcuts import redirect, render
from bde.env import EnvConfig
from utils.views import common_data

env = EnvConfig()


def admin_redirect_view(request):
    return redirect(f"/{env.ADMIN_URL}")


def legal(request):
    return render(
        request,
        "legal.html",
        {**common_data()},
    )
