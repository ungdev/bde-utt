from django.contrib import admin
from .models import Team, UserTeam, UserProfile


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(UserTeam)
class UserTeamAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "team")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "picture", "feminine_role", "description")
