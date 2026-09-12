from decimal import Decimal

from django.db import transaction

from apps.customers.backend.constants import ClienteEstado
from apps.customers.backend.repositories import ClienteRepository
from apps.inventory.backend.constants import ArticuloEstado
from apps.inventory.backend.repositories import (
    ArticuloRepository,
    ItemInventarioRepository,
)
from apps.orders.backend.constants import PedidoEstado

from .exceptions import (
    ArticuloInactivoException,
    ArticuloNoEncontradoException,
    CambioEstadoInvalidoException,
    CantidadInvalidaException,
    ClienteInactivoException,
    ClienteNoEncontradoException,
    PedidoInvalidoException,
    PedidoItemInvalidoException,
    PedidoNoEncontradoException,
    PedidoSinItemsException,
    PedidoYaEntregadoException,
    PrecioVentaInvalidoException,
    ProductoDuplicadoException,
    StockInsuficienteException,
)
from .repositories import (
    PedidoItemRepository,
    PedidoRepository,
)


class OrderService:

    @staticmethod
    def get_pedido(pedido_id):
        return PedidoRepository.get_required(pedido_id)

    @staticmethod
    def list_pedidos():
        return PedidoRepository.list_all()

    @staticmethod
    def list_pedidos_by_cliente(cliente_id):
        cliente = ClienteRepository.get_by_id(cliente_id)

        if cliente is None:
            raise ClienteNoEncontradoException(
                "El cliente no existe."
            )

        return PedidoRepository.list_by_cliente(cliente)

    @staticmethod
    def list_pedidos_by_estado(estado):
        return PedidoRepository.list_by_estado(estado)

    @staticmethod
    def get_items(pedido_id):
        pedido = PedidoRepository.get_required(pedido_id)

        return PedidoItemRepository.list_by_pedido(pedido)

    @staticmethod
    def get_item(item_id):
        return PedidoItemRepository.get_required(item_id)

    @classmethod
    def _get_cliente_activo(cls, cliente_id):
        cliente = ClienteRepository.get_by_id(cliente_id)

        if cliente is None:
            raise ClienteNoEncontradoException(
                "El cliente no existe."
            )

        if cliente.estado != ClienteEstado.ACTIVO:
            raise ClienteInactivoException(
                "El cliente está inactivo y no puede utilizarse "
                "para crear un pedido."
            )

        return cliente

    @staticmethod
    def _get_articulo_activo(articulo_id):
        articulo = ArticuloRepository.get_by_id(articulo_id)

        if articulo is None:
            raise ArticuloNoEncontradoException(
                "El artículo no existe."
            )

        if articulo.estado != ArticuloEstado.ACTIVO:
            raise ArticuloInactivoException(
                "El artículo está inactivo y no puede incluirse "
                "en un pedido."
            )

        return articulo

    @staticmethod
    def _normalize_items(items):
        if not items:
            raise PedidoSinItemsException(
                "El pedido debe contener al menos un producto."
            )

        normalized_items = []
        articulos_ids = set()

        for item in items:
            if not isinstance(item, dict):
                raise PedidoItemInvalidoException(
                    "Cada producto del pedido debe ser válido."
                )

            if "articulo_id" not in item:
                raise PedidoItemInvalidoException(
                    "Cada producto debe indicar un artículo."
                )

            articulo_id = item["articulo_id"]

            if articulo_id in articulos_ids:
                raise ProductoDuplicadoException(
                    "El mismo artículo no puede repetirse "
                    "dentro del pedido."
                )

            articulos_ids.add(articulo_id)

            try:
                cantidad = Decimal(
                    str(item.get("cantidad"))
                )
            except (TypeError, ValueError):
                raise CantidadInvalidaException(
                    "La cantidad del producto no es válida."
                )

            if cantidad <= 0:
                raise CantidadInvalidaException(
                    "La cantidad debe ser mayor que cero."
                )

            try:
                precio_venta = Decimal(
                    str(item.get("precio_venta"))
                )
            except (TypeError, ValueError):
                raise PrecioVentaInvalidoException(
                    "El precio de venta no es válido."
                )

            if precio_venta < 0:
                raise PrecioVentaInvalidoException(
                    "El precio de venta no puede ser negativo."
                )

            normalized_items.append(
                {
                    "articulo_id": articulo_id,
                    "cantidad": cantidad,
                    "precio_venta": precio_venta,
                }
            )

        return normalized_items

    @classmethod
    @transaction.atomic
    def create_pedido(
        cls,
        *,
        cliente_id,
        items,
    ):
        cliente = cls._get_cliente_activo(cliente_id)

        items = cls._normalize_items(items)

        pedido = PedidoRepository.create(
            cliente=cliente,
            estado=PedidoEstado.ENTREGADO,
        )

        for item_data in items:
            articulo = cls._get_articulo_activo(
                item_data["articulo_id"]
            )

            cantidad = item_data["cantidad"]
            precio_venta = item_data["precio_venta"]

      

            subtotal = cantidad * precio_venta

            PedidoItemRepository.create(
                pedido=pedido,
                articulo=articulo,
                sku=articulo.sku,
                cantidad=cantidad,
                precio_venta=precio_venta,
                subtotal=subtotal,
            )

        return pedido

  
    @staticmethod
    def get_total(pedido_id):
        pedido = PedidoRepository.get_required(
            pedido_id
        )

        return sum(
            (
                item.subtotal
                for item in PedidoItemRepository.list_by_pedido(
                    pedido
                )
            ),
            Decimal("0"),
        )

    @classmethod
    @transaction.atomic
    def cancel_pedido(cls, pedido_id):
        pedido = PedidoRepository.get_required(
            pedido_id
        )

        if pedido.estado == PedidoEstado.CANCELADO:
            return pedido

        if pedido.estado == PedidoEstado.ENTREGADO:
            raise CambioEstadoInvalidoException(
                "Un pedido entregado no puede cancelarse "
                "automáticamente."
            )

        raise CambioEstadoInvalidoException(
            "El estado actual del pedido no permite "
            "cancelar el pedido."
        )

    @classmethod
    @transaction.atomic
    def deliver_pedido(cls, pedido_id):
        pedido = PedidoRepository.get_required(
            pedido_id
        )

        if pedido.estado == PedidoEstado.ENTREGADO:
            raise PedidoYaEntregadoException(
                "El pedido ya se encuentra entregado."
            )

        if pedido.estado != PedidoEstado.CANCELADO:
            raise CambioEstadoInvalidoException(
                "El estado actual del pedido no permite "
                "entregarlo."
            )

        raise CambioEstadoInvalidoException(
            "Un pedido cancelado no puede convertirse "
            "automáticamente en entregado."
        )