from django.shortcuts import render
from utils.views import common_data
from core.models import Setting
from .models import UsefulContact, BDEEmail, BDEPhone


EVENTS_SEO_BY_PARAM: dict[str, dict[str, str]] = {
    "integration": {
        "title": "BDE UTT | Week-end Integration",
        "description": "Programme, infos pratiques et conseils pour le week-end d'integration organise par le BDE UTT.",
    },
    "r2d": {
        "title": "BDE UTT | R2D",
        "description": "Decouvrez la R2D, un evenement phare du BDE UTT et de la vie etudiante.",
    },
    "sdf": {
        "title": "BDE UTT | SDF",
        "description": "Informations sur la SDF, un evenement organise par le BDE UTT.",
    },
}


SERVICES_SEO_BY_PARAM: dict[str, dict[str, str]] = {
    "campus": {
        "title": "BDE UTT | Campus",
        "description": "La vie de Campus du l'UTT pour simplifier votre quotidien etudiant.",
    },
    "clubs": {
        "title": "BDE UTT | Clubs et Assos",
        "description": "Retrouvez les informations sur la gestion des clubs et associations de l'UTT ainsi que les contacts utiles proposes par le BDE.",
    },
    "communication": {
        "title": "BDE UTT | Communication",
        "description": "Les actions de communication du BDE UTT pour informer les etudiants.",
    },
    "foyer": {
        "title": "BDE UTT | Foyer",
        "description": "Decouvrez le foyer de l'UTT et les services proposes par le BDE.",
    },
    "loan": {
        "title": "BDE UTT | Pret de materiel",
        "description": "Consultez les modalites de pret de materiel proposees par le BDE UTT.",
    },
    "tickets": {
        "title": "BDE UTT | Plateforme Tickets",
        "description": "Utilisez la plateforme tickets de l'UNG pour demander un support rapide.",
    },
    "treasury": {
        "title": "BDE UTT | Tresorerie",
        "description": "Informations de tresorerie et accompagnement financier proposes par le BDE UTT.",
    },
    "zeshop": {
        "title": "BDE UTT | ZeShop",
        "description": "Decouvrez ZeShop, la boutique du BDE UTT et ses produits pour les etudiants.",
    },
}


def _seo_for_param(
    mapping: dict[str, dict[str, str]],
    param: str,
    title_prefix: str,
    description_prefix: str,
) -> dict[str, str]:
    seo = mapping.get(param)
    if seo is not None:
        return seo

    readable_param = param.replace("-", " ").title()
    return {
        "title": f"BDE UTT | {title_prefix} {readable_param}",
        "description": f"{description_prefix} {readable_param} proposé par le BDE UTT.",
    }


def home(request):
    return render(
        request,
        "home/main.html",
        {
            **common_data(
                request,
                seo={
                    "title": "BDE UTT | Accueil",
                    "description": "Bienvenue sur le site du BDE UTT : vie etudiante, evenements, services et actualites associatives.",
                },
            )
        },
    )


def contacts(request):
    return render(
        request,
        "contacts/main.html",
        {
            **common_data(
                request,
                seo={
                    "title": "BDE UTT | Contacts",
                    "description": "Retrouvez les adresses email et les numeros utiles du Bureau des Etudiants de l'UTT.",
                },
            ),
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
                **common_data(
                    request,
                    seo={
                        "title": "BDE UTT | Evenements",
                        "description": "Decouvrez les evenements du BDE UTT et consultez le calendrier associatif.",
                    },
                ),
                **_get_google_calendar_settings(),
            },
        )

    param_seo = _seo_for_param(
        EVENTS_SEO_BY_PARAM,
        param,
        "Evenement",
        "Informations sur l'evenement",
    )
    return render(
        request,
        f"events/{param}/main.html",
        {
            **common_data(
                request,
                seo=param_seo,
            )
        },
    )


def membership(request):
    return render(
        request,
        "membership/main.html",
        {
            **common_data(
                request,
                seo={
                    "title": "BDE UTT | Adhesion",
                    "description": "Toutes les informations pour adherer au BDE UTT et profiter des services associes.",
                },
            )
        },
    )


def partners(request):
    return render(
        request,
        "partners/main.html",
        {
            **common_data(
                request,
                seo={
                    "title": "BDE UTT | Partenaires",
                    "description": "Decouvrez les partenaires du BDE UTT et les avantages proposes aux etudiants.",
                },
            )
        },
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
            {
                **common_data(
                    request,
                    seo={
                        "title": "BDE UTT | Services",
                        "description": "Explorez les services du BDE UTT pour faciliter votre vie etudiante.",
                    },
                )
            },
        )

    param_seo = _seo_for_param(
        SERVICES_SEO_BY_PARAM,
        param,
        "Service",
        "Details du service",
    )
    return render(
        request,
        f"services/{param}/main.html",
        {
            **common_data(
                request,
                seo=param_seo,
            ),
            **_get_userful_contacts(param),
        },
    )
