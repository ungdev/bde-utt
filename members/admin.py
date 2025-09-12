from django.contrib import admin
from .models import Team, MemberProfile


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "team")
