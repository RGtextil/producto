from django.contrib import admin

from .backend.models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "numero_documento",
        "nombre",
        "apellido",
        "tipo_documento",
        "telefono",
        "email",
        "limite_credito",
        "estado",
        "created_at",
    )

    list_filter = (
        "estado",
        "tipo_documento",
    )

    search_fields = (
        "numero_documento",
        "nombre",
        "apellido",
        "telefono",
        "email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = (
        "nombre",
        "apellido",
        "id",
    )
