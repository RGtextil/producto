from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from .constants import DeudaTipo, OtroDineroTipo


class OtroDinero(models.Model):
    nombre = models.CharField(
        max_length=150,
    )
    tipo = models.CharField(
        max_length=10,
        choices=OtroDineroTipo.choices,
        default=OtroDineroTipo.OTRO,
        db_index=True,
    )
    concepto = models.CharField(
        max_length=255,
    )
    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
        ],
    )
    fecha = models.DateField()
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-fecha", "-id"]
        indexes = [
            models.Index(fields=["tipo"]),
            models.Index(fields=["fecha"]),
        ]

    def __str__(self):
        return f"{self.nombre} - {self.monto}"


class Deuda(models.Model):
    nombre = models.CharField(
        max_length=150,
    )
    tipo = models.CharField(
        max_length=10,
        choices=DeudaTipo.choices,
        default=DeudaTipo.OTRO,
        db_index=True,
    )
    concepto = models.CharField(
        max_length=255,
    )
    monto = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01")),
        ],
    )
    fecha = models.DateField()
    fecha_vencimiento = models.DateField(
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-fecha", "-id"]
        indexes = [
            models.Index(fields=["tipo"]),
            models.Index(fields=["fecha"]),
            models.Index(fields=["fecha_vencimiento"]),
        ]

    def __str__(self):
        return f"{self.nombre} - {self.monto}"