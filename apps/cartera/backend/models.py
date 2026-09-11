from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from apps.orders.backend.models import Pedido

from .constants import CarteraEstado, CarteraTipo


class Cartera(models.Model):
    pedido = models.OneToOneField(
        Pedido,
        on_delete=models.PROTECT,
        related_name="cartera",
        null=True,
        blank=True,
    )
    tipo = models.CharField(
        max_length=10,
        choices=CarteraTipo.choices,
        default=CarteraTipo.PEDIDO,
        db_index=True,
    )
    nombre = models.CharField(
        max_length=150,
    )
    concepto = models.CharField(
        max_length=255,
    )
    fecha_inicio = models.DateField()
    fecha_vencimiento = models.DateField(
        null=True,
        blank=True,
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0")),
        ],
    )
    estado = models.CharField(
        max_length=10,
        choices=CarteraEstado.choices,
        default=CarteraEstado.PENDIENTE,
        db_index=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-fecha_inicio", "-id"]
        indexes = [
            models.Index(fields=["tipo"]),
            models.Index(fields=["estado"]),
            models.Index(fields=["fecha_inicio"]),
            models.Index(fields=["fecha_vencimiento"]),
        ]

    def __str__(self):
        return f"{self.nombre} - {self.total}"

    @property
    def total_abonos(self):
        return sum(
            (
                abono.monto
                for abono in self.abonos.all()
            ),
            Decimal("0"),
        )

    @property
    def saldo(self):
        return max(
            self.total - self.total_abonos,
            Decimal("0"),
        )


class Abono(models.Model):
    cartera = models.ForeignKey(
        Cartera,
        on_delete=models.CASCADE,
        related_name="abonos",
    )
    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
        ],
    )
    fecha = models.DateField()
    concepto = models.CharField(
        max_length=255,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-fecha", "-id"]
        indexes = [
            models.Index(fields=["cartera"]),
            models.Index(fields=["fecha"]),
        ]

    def __str__(self):
        return f"Abono {self.monto} - {self.cartera.nombre}"