from django.contrib import admin
from .models import Partner, BDEEmail, BDEPhone, UsefulContact


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


@admin.register(BDEEmail)
class BDEEmailAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Adresse email du BDE",
            {
                "description": 'Cette section permet de gérer les adresses email affichées sur la page "Contacts".',
                "fields": ("name", "email"),
            },
        ),
    )

    list_display = ("name", "email")


@admin.register(BDEPhone)
class BDEPhoneAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Numéros de téléphone du BDE",
            {
                "description": 'Cette section permet de gérer les numéros de téléphone affichés sur la page "Contacts".',
                "fields": ("name", "phone_number"),
            },
        ),
    )

    list_display = ("name", "phone_number")


@admin.register(UsefulContact)
class UsefulContactAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            "Contact utile",
            {
                "description": 'Cette section permet de gérer les contacts utiles affichés sur la page "Services / Clubs & Assos".',
                "fields": ("name", "email"),
            },
        ),
    )

    list_display = ("name", "email")
