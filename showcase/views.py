from django.shortcuts import render
from utils.views import common_data


def home(request):
    return render(
        request,
        "home/main.html",
        {**common_data()},
    )


def contacts(request):
    return render(
        request,
        "contacts/main.html",
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
        f"events/{param}/main.html",
        {**common_data()},
    )


def membership(request):
    return render(
        request,
        "membership/main.html",
        {**common_data()},
    )


def partners(request):
    return render(
        request,
        "partners/main.html",
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
        f"services/{param}/main.html",
        {**common_data()},
    )
