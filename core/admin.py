from django.contrib import admin
from .models import Setting, Page, TextArea


@admin.register(Setting)
class SettingAdmin(admin.ModelAdmin):
    list_display = ("key", "value")

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("path", "title", "description")
    search_fields = ("path", "title", "description", "seo_title", "seo_description")

@admin.register(TextArea)
class TextAreaAdmin(admin.ModelAdmin):
    list_display = ("key", "page", "content")
    list_filter = ("page__path",)
    search_fields = ("key", "content")
