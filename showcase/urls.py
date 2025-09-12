from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path("services/", views.services, name="services"),
    path("services/<str:param>/", views.services, name="services"),
    path("membership/", views.membership, name="membership"),
    path("partners/", views.partners, name="partners"),
]
