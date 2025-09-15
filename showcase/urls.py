from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path("events/", views.events, name="events"),
    path("events/<str:param>/", views.events, name="events"),
    path("membership/", views.membership, name="membership"),
    path("partners/", views.partners, name="partners"),
    path("services/", views.services, name="services"),
    path("services/<str:param>/", views.services, name="services"),
]
