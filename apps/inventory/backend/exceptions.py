class InventoryException(Exception):
    """Excepción base del módulo de inventario."""


class ArticuloException(InventoryException):
    """Error relacionado con un artículo."""


class ArticuloDuplicadoException(ArticuloException):
    """El artículo ya existe."""


class ArticuloNoEncontradoException(ArticuloException):
    """El artículo solicitado no existe."""


class ArticuloInactivoException(ArticuloException):
    """El artículo está inactivo y no puede utilizarse."""


class SKUInvalidoException(ArticuloException):
    """El SKU no cumple las reglas del inventario."""


class StockInsuficienteException(InventoryException):
    """No existe suficiente stock disponible."""


class StockInvalidoException(InventoryException):
    """La cantidad de inventario no es válida."""


class ItemInventarioNoEncontradoException(InventoryException):
    """El registro de inventario solicitado no existe."""

class InventoryException(Exception):
    """Excepción base del módulo de inventario."""


class ArticuloException(InventoryException):
    """Error relacionado con un artículo."""


class ArticuloDuplicadoException(ArticuloException):
    """El artículo ya existe."""


class ArticuloNoEncontradoException(ArticuloException):
    """El artículo solicitado no existe."""


class ArticuloInactivoException(ArticuloException):
    """El artículo está inactivo y no puede utilizarse."""


class SKUInvalidoException(ArticuloException):
    """El SKU no cumple las reglas del inventario."""


class StockInsuficienteException(InventoryException):
    """No existe suficiente stock disponible."""


class StockInvalidoException(InventoryException):
    """La cantidad de inventario no es válida."""


class ItemInventarioNoEncontradoException(InventoryException):
    """El registro de inventario solicitado no existe."""


class ArticuloConInventarioException(ArticuloException):
    """El artículo tiene registros de inventario asociados."""