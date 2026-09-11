class OrderException(Exception):
    """Excepción base del módulo de pedidos."""


class PedidoException(OrderException):
    """Error relacionado con un pedido."""


class PedidoNoEncontradoException(PedidoException):
    """El pedido solicitado no existe."""


class PedidoInvalidoException(PedidoException):
    """El pedido no cumple las reglas de negocio."""


class PedidoSinItemsException(PedidoException):
    """El pedido no contiene productos."""


class PedidoItemInvalidoException(PedidoException):
    """Un producto del pedido no cumple las reglas de negocio."""


class ClienteNoEncontradoException(PedidoException):
    """El cliente solicitado no existe."""


class ClienteInactivoException(PedidoException):
    """El cliente está inactivo y no puede realizar pedidos."""


class ArticuloNoEncontradoException(PedidoException):
    """El artículo solicitado no existe."""


class ArticuloInactivoException(PedidoException):
    """El artículo está inactivo y no puede incluirse en un pedido."""


class StockInsuficienteException(PedidoException):
    """No existe suficiente inventario para completar el pedido."""


class CantidadInvalidaException(PedidoException):
    """La cantidad de un producto no es válida."""


class PrecioVentaInvalidoException(PedidoException):
    """El precio de venta no es válido."""


class ProductoDuplicadoException(PedidoException):
    """El mismo artículo no puede repetirse dentro del pedido."""


class PedidoCanceladoException(PedidoException):
    """El pedido está cancelado y no puede modificarse."""


class PedidoYaEntregadoException(PedidoException):
    """El pedido ya se encuentra entregado."""

class  PedidoItemNoEncontradoException(PedidoException):
    """el pedido item no se encuentra"""


class CambioEstadoInvalidoException(PedidoException):
    """El cambio de estado solicitado no está permitido."""