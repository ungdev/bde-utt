from django.contrib import admin
from .models import Partner


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "url", "enable")
    actions = [
        "make_enabled",
        "make_disabled",
        "decrement_order",
        "increment_order",
        "reset_order",
    ]

    @admin.action(description="Montrer")
    def make_enabled(self, request, queryset):
        queryset.update(enable=True)

    @admin.action(description="Cacher")
    def make_disabled(self, request, queryset):
        queryset.update(enable=False)

    @admin.action(description="Avancer de 1")
    def decrement_order(self, request, queryset):
        for partner in queryset:
            partner.order -= 1
            partner.save()

    @admin.action(description="Reculer de 1")
    def increment_order(self, request, queryset):
        for partner in queryset:
            partner.order += 1
            partner.save()

    @admin.action(description="Réinitialiser l'ordre")
    def reset_order(self, request, queryset):
        queryset.update(order=0)
