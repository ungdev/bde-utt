from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from bde.env import EnvConfig

env = EnvConfig()
ADMIN_URL = env.ADMIN_URL


urlpatterns = [
    path("", include("showcase.urls")),
    path("legals", __import__("bde.views").views.legals),
    path("logout", __import__("bde.views").views.admin_logout),
    path("members/", include("members.urls")),
    path("privacy", __import__("bde.views").views.privacy),
    path("redirect/admin/", __import__("bde.views").views.admin_redirect_view),
    path(
        "robots.txt",
        serve,
        {"path": "robots.txt", "document_root": settings.STATIC_ROOT},
    ),
    path("sso/", include("mozilla_django_oidc.urls")),
    path(ADMIN_URL, admin.site.urls),
]

# Expose uploads folder in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
