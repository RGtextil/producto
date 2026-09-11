from django.contrib import admin

from .backend.models import Abono, Cartera


@admin.register(Cartera)
class CarteraAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nombre",
        "tipo",
        "pedido",
        "fecha_inicio",
        "fecha_vencimiento",
        "total",
        "estado",
        "created_at",
    )
    list_filter = (
        "tipo",
        "estado",
        "fecha_inicio",
    )
    search_fields = (
        "nombre",
        "concepto",
        "pedido__id",
        "pedido__cliente__nombre",
        "pedido__cliente__apellido",
        "pedido__cliente__numero_documento",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "-fecha_inicio",
        "-id",
    )


@admin.register(Abono)
class AbonoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cartera",
        "monto",
        "fecha",
        "concepto",
        "created_at",
    )
    list_filter = (
        "fecha",
    )
    search_fields = (
        "cartera__nombre",
        "cartera__concepto",
        "concepto",
    )
    readonly_fields = (
        "created_at",
    )
    ordering = (
        "-fecha",
        "-id",
    )