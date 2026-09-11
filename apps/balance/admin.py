from django.contrib import admin

from .backend.models import Deuda, OtroDinero


@admin.register(OtroDinero)
class OtroDineroAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "tipo",
        "concepto",
        "monto",
        "fecha",
        "created_at",
    )

    list_filter = (
        "tipo",
        "fecha",
    )

    search_fields = (
        "nombre",
        "concepto",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-fecha",
        "-id",
    )


@admin.register(Deuda)
class DeudaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "tipo",
        "concepto",
        "monto",
        "fecha",
        "fecha_vencimiento",
        "created_at",
    )

    list_filter = (
        "tipo",
        "fecha",
        "fecha_vencimiento",
    )

    search_fields = (
        "nombre",
        "concepto",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "-fecha",
        "-id",
    )