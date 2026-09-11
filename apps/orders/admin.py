from django.contrib import admin

from .backend.models import Pedido, PedidoItem


class PedidoItemInline(admin.TabularInline):
    model = PedidoItem
    extra = 0

    fields = (
        "articulo",
        "sku",
        "cantidad",
        "precio_venta",
        "subtotal",
    )

    readonly_fields = (
        "cantidad",
        "precio_venta",
        "subtotal",
    )


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cliente",
        "estado",
        "total",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "estado",
        "created_at",
    )

    search_fields = (
        "cliente__nombre",
        "cliente__apellido",
        "cliente__numero_documento",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "total",
    )

    ordering = (
        "-created_at",
        "-id",
    )

    inlines = (
        PedidoItemInline,
    )


@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "pedido",
        "articulo",
        "cantidad",
        "precio_venta",
        "subtotal",
    )

    list_filter = (
        "articulo",
    )

    search_fields = (
        "articulo__descripcion",
        "articulo__sku",
        "pedido__cliente__nombre",
        "pedido__cliente__apellido",
        "pedido__cliente__numero_documento",
    )

    readonly_fields = (
        "cantidad",
        "precio_venta",
        "subtotal",
        "pedido",
        "articulo",
    )

    ordering = (
        "-pedido__created_at",
        "id",
    )