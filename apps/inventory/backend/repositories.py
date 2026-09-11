from django.db.models import Sum

from .models import Articulo, ItemInventario
from django.db.models import F, Sum

class ArticuloRepository:
    """Acceso a datos de Articulo."""

    @staticmethod
    def get_by_id(articulo_id):
        return (
            Articulo.objects
            .filter(pk=articulo_id)
            .first()
        )

    @staticmethod
    def get_by_sku(sku):
        return (
            Articulo.objects
            .filter(sku=sku)
            .first()
        )

    @staticmethod
    def exists_by_sku(sku):
        return Articulo.objects.filter(sku=sku).exists()

    @staticmethod
    def create(**data):
        return Articulo.objects.create(**data)

    @staticmethod
    def update(articulo, **data):
        for field, value in data.items():
            setattr(articulo, field, value)

        articulo.save(
            update_fields=[
                *data.keys(),
                "updated_at",
            ]
        )

        return articulo

    @staticmethod
    def list_all():
        return (
            Articulo.objects
            .prefetch_related("items_inventario")
            .all()
        )

    @staticmethod
    def list_active():
        return (
            Articulo.objects
            .filter(estado="ACTIVO")
            .prefetch_related("items_inventario")
        )

    @staticmethod
    def delete(articulo):
        articulo.delete()


class ItemInventarioRepository:
    """Acceso a datos de ItemInventario."""

    @staticmethod
    def get_by_id(item_id):
        return (
            ItemInventario.objects
            .select_related("articulo")
            .filter(pk=item_id)
            .first()
        )

    @staticmethod
    def get_by_articulo(articulo):
        return (
            ItemInventario.objects
            .filter(articulo=articulo)
            .first()
        )

    @staticmethod
    def list_by_articulo(articulo):
        return (
            ItemInventario.objects
            .filter(articulo=articulo)
            .order_by("id")
        )

    @staticmethod
    def create(**data):
        return ItemInventario.objects.create(**data)

    @staticmethod
    def update(item, **data):
        for field, value in data.items():
            setattr(item, field, value)

        item.save(
            update_fields=[
                *data.keys(),
                "updated_at",
            ]
        )

        return item

    @staticmethod
    def delete(item):
        item.delete()

    @staticmethod
    def get_stock(articulo):
        result = (
            ItemInventario.objects
            .filter(articulo=articulo)
            .aggregate(total=Sum("cantidad"))
        )

        return result["total"] or 0
    
    @staticmethod
    def get_total_valor_inventario():
        result = ItemInventario.objects.aggregate(
            total=Sum(
                F("cantidad") * F("articulo__costo_base")
            )
        )

        return result["total"] or 0