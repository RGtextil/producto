from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.customers.backend.models import Cliente
from apps.inventory.backend.models import Articulo

from .constants import PedidoEstado


class Pedido(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="pedidos",
    )
    estado = models.CharField(
        max_length=10,
        choices=PedidoEstado.choices,
        default=PedidoEstado.ENTREGADO,
        db_index=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [
            models.Index(fields=["cliente"]),
            models.Index(fields=["estado"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"

    @property
    def total(self):
        return sum(
            (
                item.subtotal
                for item in self.items.all()
            ),
            Decimal("0"),
        )


class PedidoItem(models.Model):
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name="items",
    )
    articulo = models.ForeignKey(
        Articulo,
        on_delete=models.PROTECT,
        related_name="items_pedido",
    )
    sku = models.CharField(
        max_length=150,
    )
    cantidad = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
        ],
    )
    precio_venta = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0")),
        ],
    )
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0")),
        ],
    )

    class Meta:
        ordering = ["id"]
        indexes = [
            models.Index(fields=["pedido"]),
            models.Index(fields=["articulo"]),
        ]

    def __str__(self):
        return (
            f"{self.pedido} - "
            f"{self.sku} - "
            f"{self.cantidad}"
        )
