from .exceptions import (
    PedidoNoEncontradoException,
    PedidoItemNoEncontradoException,
)
from .models import Pedido, PedidoItem


class PedidoRepository:

    @staticmethod
    def get_by_id(pedido_id):
        return (
            Pedido.objects
            .select_related("cliente")
            .filter(pk=pedido_id)
            .first()
        )

    @staticmethod
    def get_required(pedido_id):
        pedido = PedidoRepository.get_by_id(pedido_id)

        if pedido is None:
            raise PedidoNoEncontradoException(
                "El pedido no existe."
            )

        return pedido

    @staticmethod
    def create(**data):
        return Pedido.objects.create(**data)

    @staticmethod
    def update(pedido, **data):
        for field, value in data.items():
            setattr(pedido, field, value)

        pedido.save(
            update_fields=[
                *data.keys(),
                "updated_at",
            ]
        )

        return pedido

    @staticmethod
    def list_all():
        return (
            Pedido.objects
            .select_related("cliente")
            .prefetch_related("items")
            .all()
        )

    @staticmethod
    def list_by_cliente(cliente):
        return (
            Pedido.objects
            .filter(cliente=cliente)
            .select_related("cliente")
            .prefetch_related("items")
            .all()
        )

    @staticmethod
    def list_by_estado(estado):
        return (
            Pedido.objects
            .filter(estado=estado)
            .select_related("cliente")
            .prefetch_related("items")
            .all()
        )

    @staticmethod
    def delete(pedido):
        pedido.delete()


class PedidoItemRepository:

    @staticmethod
    def get_by_id(item_id):
        return (
            PedidoItem.objects
            .select_related(
                "pedido",
                "pedido__cliente",
                "articulo",
            )
            .filter(pk=item_id)
            .first()
        )

    @staticmethod
    def get_required(item_id):
        item = PedidoItemRepository.get_by_id(item_id)

        if item is None:
            raise PedidoItemNoEncontradoException(
                "El producto del pedido no existe."
            )

        return item

    @staticmethod
    def create(**data):
        return PedidoItem.objects.create(**data)

    @staticmethod
    def update(item, **data):
        for field, value in data.items():
            setattr(item, field, value)

        item.save(
            update_fields=[
                *data.keys(),
            ]
        )

        return item

    @staticmethod
    def list_by_pedido(pedido):
        return (
            PedidoItem.objects
            .filter(pedido=pedido)
            .select_related("articulo")
            .order_by("id")
        )

    @staticmethod
    def get_by_pedido_and_articulo(pedido, articulo):
        return (
            PedidoItem.objects
            .filter(
                pedido=pedido,
                articulo=articulo,
            )
            .first()
        )

    @staticmethod
    def delete(item):
        item.delete()