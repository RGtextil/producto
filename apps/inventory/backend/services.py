import re
import unicodedata
from decimal import Decimal

from django.db import transaction
from apps.inventory.backend.repositories import ItemInventarioRepository
from .constants import ArticuloEstado
from .exceptions import (
    ArticuloDuplicadoException,
    ArticuloInactivoException,
    ArticuloNoEncontradoException,
    ItemInventarioNoEncontradoException,
    SKUInvalidoException,
    StockInvalidoException,
    StockInsuficienteException,
)
from .repositories import (
    ArticuloRepository,
    ItemInventarioRepository,
)


class InventoryService:
    """Reglas de negocio del módulo de inventario."""

    @staticmethod
    def _normalize_text(value):
        """
        Normaliza texto para utilizarlo en la generación del SKU.
        """
        value = str(value or "").strip().upper()

        value = unicodedata.normalize(
            "NFKD",
            value,
        )

        value = "".join(
            char
            for char in value
            if not unicodedata.combining(char)
        )

        value = re.sub(
            r"[^A-Z0-9]+",
            "-",
            value,
        )

        return value.strip("-")

    @classmethod
    def generate_sku(
        cls,
        descripcion,
        clasificacion,
        unidad_medida,
        color="",
    ):
        """
        Genera el SKU a partir de los datos del artículo.
        """

        parts = [
            cls._normalize_text(descripcion),
            cls._normalize_text(clasificacion),
            cls._normalize_text(unidad_medida),
        ]

        normalized_color = cls._normalize_text(color)

        if normalized_color:
            parts.append(normalized_color)

        sku = "-".join(
            part
            for part in parts
            if part
        )

        if not sku:
            raise SKUInvalidoException(
                "No fue posible generar un SKU válido."
            )

        if len(sku) > 150:
            raise SKUInvalidoException(
                "El SKU generado supera la longitud permitida."
            )

        return sku

    @classmethod
    @transaction.atomic
    def create_articulo(
        cls,
        *,
        descripcion,
        clasificacion,
        unidad_medida,
        costo_base,
        alerta_minimo,
        ubicacion_almacen="",
        color="",
    ):
        """
        Crea un artículo y genera automáticamente su SKU.
        """

        sku = cls.generate_sku(
            descripcion=descripcion,
            clasificacion=clasificacion,
            unidad_medida=unidad_medida,
            color=color,
        )

        if ArticuloRepository.exists_by_sku(sku):
            raise ArticuloDuplicadoException(
                "Ya existe un artículo con los mismos datos "
                "que generan este SKU."
            )

        return ArticuloRepository.create(
            sku=sku,
            descripcion=descripcion.strip(),
            clasificacion=clasificacion,
            unidad_medida=unidad_medida,
            costo_base=costo_base,
            alerta_minimo=alerta_minimo,
            ubicacion_almacen=ubicacion_almacen.strip(),
            color=color.strip(),
            estado=ArticuloEstado.ACTIVO,
        )

    
    @staticmethod
    def list_descripciones_disponibles():
        return ArticuloRepository.list_active_descriptions()

    @staticmethod
    def list_colores_by_descripcion(descripcion):
        descripcion = str(descripcion or "").strip()

        if not descripcion:
            return []

        return ArticuloRepository.list_active_colors_by_description(
            descripcion
        )

    @staticmethod
    def get_articulo_by_descripcion_and_color(
        descripcion,
        color,
    ):
        descripcion = str(descripcion or "").strip()
        color = str(color or "").strip()

        if not descripcion:
            raise ArticuloNoEncontradoException(
                "La descripción del artículo es obligatoria."
            )

        if not color:
            raise ArticuloNoEncontradoException(
                "El color del artículo es obligatorio."
            )

        articulo = (
            ArticuloRepository
            .get_active_by_description_and_color(
                descripcion,
                color,
            )
        )

        if articulo is None:
            raise ArticuloNoEncontradoException(
                "No existe un artículo activo con "
                "la descripción y color seleccionados."
            )

        return articulo

    @staticmethod
    def get_articulo(articulo_id):
        articulo = ArticuloRepository.get_by_id(
            articulo_id
        )

        if articulo is None:
            raise ArticuloNoEncontradoException(
                "El artículo no existe."
            )

        return articulo

    @staticmethod
    def get_articulo_by_sku(sku):
        articulo = ArticuloRepository.get_by_sku(
            sku
        )

        if articulo is None:
            raise ArticuloNoEncontradoException(
                "El artículo no existe."
            )

        return articulo


    @staticmethod
    def list_articulos():
        return ArticuloRepository.list_all()

    @staticmethod
    def list_articulos_activos():
        return ArticuloRepository.list_active()

    @staticmethod
    @transaction.atomic
    def update_articulo(
        cls,
        articulo_id,
        *,
        costo_base=None,
        alerta_minimo=None,
        ubicacion_almacen=None,
        estado=None,
    ):
        """
        Actualiza únicamente información que no modifica
        la identidad utilizada para generar el SKU.

        El SKU se mantiene inmutable después de crear el artículo.
        """

        articulo = cls.get_articulo(articulo_id)

        data = {}

        if costo_base is not None:
            data["costo_base"] = costo_base

        if alerta_minimo is not None:
            data["alerta_minimo"] = alerta_minimo

        if ubicacion_almacen is not None:
            data["ubicacion_almacen"] = (
                ubicacion_almacen.strip()
            )

        if estado is not None:
            data["estado"] = estado

        if not data:
            return articulo

        return ArticuloRepository.update(
            articulo,
            **data,
        )

    @staticmethod
    @transaction.atomic
    def deactivate_articulo(articulo_id):
        articulo = InventoryService.get_articulo(
            articulo_id
        )

        if articulo.estado == ArticuloEstado.INACTIVO:
            return articulo

        return ArticuloRepository.update(
            articulo,
            estado=ArticuloEstado.INACTIVO,
        )

    @staticmethod
    @transaction.atomic
    def delete_articulo(articulo_id):
        """
        Elimina un artículo únicamente cuando no tiene
        registros de inventario asociados.

        La protección final también está respaldada por
        la relación PROTECT del modelo.
        """

        articulo = InventoryService.get_articulo(
            articulo_id
        )

        if articulo.items_inventario.exists():
            raise ArticuloDuplicadoException(
                "No se puede eliminar un artículo que "
                "tiene registros de inventario."
            )

        ArticuloRepository.delete(articulo)

    @staticmethod
    def get_stock(articulo_id):
        articulo = InventoryService.get_articulo(
            articulo_id
        )

        return ItemInventarioRepository.get_stock(
            articulo
        )

    @staticmethod
    def is_low_stock(articulo_id):
        articulo = InventoryService.get_articulo(
            articulo_id
        )

        stock = ItemInventarioRepository.get_stock(
            articulo
        )

        return stock < articulo.alerta_minimo

    @staticmethod
    def get_inventory_items(articulo_id):
        articulo = InventoryService.get_articulo(
            articulo_id
        )

        return ItemInventarioRepository.list_by_articulo(
            articulo
        )

    @staticmethod
    def get_inventory_item(item_id):
        item = ItemInventarioRepository.get_by_id(item_id)

        if item is None:
            raise ItemInventarioNoEncontradoException(
                "El registro de inventario no existe."
            )

        return item

    @staticmethod
    @transaction.atomic
    def add_inventory(
        articulo_id,
        cantidad,
        ubicacion="",
    ):
        """
        Agrega una existencia de inventario.
        """

        articulo = InventoryService.get_articulo(
            articulo_id
        )

        if articulo.estado != ArticuloEstado.ACTIVO:
            raise ArticuloInactivoException(
                "No se puede agregar inventario "
                "a un artículo inactivo."
            )

        cantidad = Decimal(str(cantidad))

        if cantidad <= 0:
            raise StockInvalidoException(
                "La cantidad debe ser mayor que cero."
            )

        return ItemInventarioRepository.create(
            articulo=articulo,
            cantidad=cantidad,
            ubicacion=ubicacion.strip(),
        )

    
    @staticmethod
    @transaction.atomic
    def update_articulo(
        articulo_id,
        *,
        costo_base=None,
        alerta_minimo=None,
        ubicacion_almacen=None,
        estado=None,
    ):
        """
        Actualiza únicamente información que no modifica
        la identidad utilizada para generar el SKU.

        El SKU se mantiene inmutable después de crear el artículo.
        """

        articulo = InventoryService.get_articulo(
            articulo_id
        )

        data = {}

        if costo_base is not None:
            data["costo_base"] = costo_base

        if alerta_minimo is not None:
            data["alerta_minimo"] = alerta_minimo

        if ubicacion_almacen is not None:
            data["ubicacion_almacen"] = (
                ubicacion_almacen.strip()
            )

        if estado is not None:
            data["estado"] = estado

        if not data:
            return articulo

        return ArticuloRepository.update(
            articulo,
            **data,
        )


 
    @staticmethod
    @transaction.atomic
    def remove_inventory(item_id):
        item = ItemInventarioRepository.get_by_id(
            item_id
        )

        if item is None:
            raise ItemInventarioNoEncontradoException(
                "El registro de inventario no existe."
            )

        ItemInventarioRepository.delete(item)

    @staticmethod
    @transaction.atomic
    def decrease_stock(
        articulo_id,
        cantidad,
    ):
        """
        Reduce el stock disponible del artículo.

        Se utiliza cuando una operación de negocio,
        como la entrega de un pedido, necesita descontar
        inventario.
        """

        articulo = InventoryService.get_articulo(
            articulo_id
        )

        if articulo.estado != ArticuloEstado.ACTIVO:
            raise ArticuloInactivoException(
                "No se puede descontar inventario "
                "de un artículo inactivo."
            )

        cantidad = Decimal(str(cantidad))

        if cantidad <= 0:
            raise StockInvalidoException(
                "La cantidad debe ser mayor que cero."
            )

        items = list(
            ItemInventarioRepository.list_by_articulo(
                articulo
            )
        )

        stock_total = sum(
            (item.cantidad for item in items),
            Decimal("0"),
        )

        if stock_total < cantidad:
            raise StockInsuficienteException(
                "No existe suficiente stock disponible."
            )

        restante = cantidad

        for item in items:
            if restante <= 0:
                break

            descuento = min(
                item.cantidad,
                restante,
            )

            nueva_cantidad = (
                item.cantidad - descuento
            )

            ItemInventarioRepository.update(
                item,
                cantidad=nueva_cantidad,
            )

            restante -= descuento

        return InventoryService.get_stock(
            articulo_id
        )
