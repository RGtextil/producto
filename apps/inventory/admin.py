from django.contrib import admin

from .backend.models import Articulo, ItemInventario

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    list_display = (
    "sku",
    "descripcion",
    "clasificacion",
    "unidad_medida",
    "costo_base",
    "alerta_minimo",
    "estado",
    )
    list_filter = (
    "estado",
    "clasificacion",
    "unidad_medida",
    )
    search_fields = (
    "sku",
    "descripcion",
    "color",
    )
    readonly_fields = (
    "sku",
    "created_at",
    "updated_at",
    )

@admin.register(ItemInventario)
class ItemInventarioAdmin(admin.ModelAdmin):
    list_display = (
    "articulo",
    "cantidad",
    "ubicacion",
    "created_at",
    "updated_at",
    )
    search_fields = (
    "articulo__sku",
    "articulo__descripcion",
    "ubicacion",
    )
    list_filter = (
    "articulo__clasificacion",
    )
    readonly_fields = (
    "created_at",
    "updated_at",
    )
