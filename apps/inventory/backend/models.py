from django.core.validators import MinValueValidator
from django.db import models

from .constants import (
    ArticuloEstado,
    ClasificacionArticulo,
    UnidadMedida,
)


class Articulo(models.Model):
    sku = models.CharField(
        max_length=150,
        unique=True,
        db_index=True,
    )
    descripcion = models.CharField(
        max_length=255,
    )
    clasificacion = models.CharField(
        max_length=30,
        choices=ClasificacionArticulo.choices,
    )
    unidad_medida = models.CharField(
        max_length=20,
        choices=UnidadMedida.choices,
    )
    costo_base = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    alerta_minimo = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    ubicacion_almacen = models.CharField(
        max_length=150,
        blank=True,
    )
    color = models.CharField(
        max_length=80,
        blank=True,
    )
    estado = models.CharField(
        max_length=10,
        choices=ArticuloEstado.choices,
        default=ArticuloEstado.ACTIVO,
        db_index=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["descripcion", "id"]
        indexes = [
            models.Index(fields=["estado"]),
            models.Index(fields=["clasificacion"]),
        ]

    def __str__(self):
        return f"{self.sku} - {self.descripcion}"


class ItemInventario(models.Model):
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.PROTECT,
        related_name="items_inventario",
    )
    cantidad = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    ubicacion = models.CharField(
        max_length=150,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["articulo__descripcion", "id"]
        indexes = [
            models.Index(fields=["articulo"]),
        ]

    def __str__(self):
        return f"{self.articulo.sku} - {self.cantidad}"

    @property
    def valor_costo(self):
        return self.cantidad * self.articulo.costo_base
