from django.shortcuts import render
from .models import News
from utils.views import common_data


def home(request):
    return render(
        request,
        "home.html",
        {
            **common_data(),
            "news": News.objects.filter(enable=True),
        },
    )


def contacts(request):
    return render(
        request,
        "contacts.html",
        {**common_data()},
    )


def events(request, param: str | None = None):
    if param is None:
        return render(
            request,
            "events/main.html",
            {**common_data()},
        )
    return render(
        request,
        f"events/{param}.html",
        {**common_data()},
    )


def membership(request):
    return render(
        request,
        "membership.html",
        {**common_data()},
    )


def partners(request):
    return render(
        request,
        "partners.html",
        {**common_data()},
    )


def services(request, param: str | None = None):
    if param is None:
        return render(
            request,
            "services/main.html",
            {**common_data()},
        )
    return render(
        request,
        f"services/{param}.html",
        {**common_data()},
    )
