from django.shortcuts import render
from utils.views import common_data
from core.models import Setting
from .models import UsefulContact, BDEEmail, BDEPhone


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
        {
            **common_data(),
            "bde_emails": BDEEmail.objects.all(),
            "bde_phones": BDEPhone.objects.all(),
        },
    )


def events(request, param: str | None = None):

    def _get_google_calendar_settings() -> dict:

        try:
            google_calendar_src = Setting.objects.get(key="google_calendar_src").value
        except Setting.DoesNotExist:
            google_calendar_src = ""

        try:
            google_calendar_mode = Setting.objects.get(key="google_calendar_mode").value
        except Setting.DoesNotExist:
            google_calendar_mode = "WEEK"

        return {
            "google_calendar_src": google_calendar_src,
            "google_calendar_mode": google_calendar_mode,
        }

    if param is None:
        return render(
            request,
            "events/main.html",
            {
                **common_data(),
                **_get_google_calendar_settings(),
            },
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

    def _get_userful_contacts(param: str) -> dict:
        if param != "clubs":
            return {}

        return {
            "useful_contacts": UsefulContact.objects.all(),
        }

    if param is None:
        return render(
            request,
            "services/main.html",
            {**common_data()},
        )
    return render(
        request,
        f"services/{param}/main.html",
        {
            **common_data(),
            **_get_userful_contacts(param),
        },
    )
