from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from bde.env import EnvConfig

env = EnvConfig()
ADMIN_URL = env.ADMIN_URL


urlpatterns = [
    path("", include("showcase.urls")),
    path("sso/", include("mozilla_django_oidc.urls")),
    path("redirect/admin/", __import__("bde.views").views.admin_redirect_view),
    path("legal", __import__("bde.views").views.legal),
    path(ADMIN_URL, admin.site.urls),
    path("members/", include("members.urls")),
]

# Expose uploads folder in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
