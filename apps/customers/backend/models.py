from django.core.validators import MinValueValidator
from django.db import models

from .constants import ClienteEstado, TipoDocumento


class Cliente(models.Model):
    tipo_documento = models.CharField(
        max_length=20,
        choices=TipoDocumento.choices,
    )
    numero_documento = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
    )
    nombre = models.CharField(
        max_length=150,
    )
    apellido = models.CharField(
        max_length=150,
        blank=True,
    )
    telefono = models.CharField(
        max_length=30,
        blank=True,
    )
    email = models.EmailField(
        max_length=254,
        blank=True,
    )
    direccion = models.CharField(
        max_length=255,
        blank=True,
    )
    ciudad = models.CharField(
        max_length=100,
        blank=True,
    )
    departamento = models.CharField(
        max_length=100,
        blank=True,
    )
    limite_credito = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    estado = models.CharField(
        max_length=10,
        choices=ClienteEstado.choices,
        default=ClienteEstado.ACTIVO,
        db_index=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["nombre", "apellido", "id"]
        indexes = [
            models.Index(fields=["estado"]),
            models.Index(fields=["nombre"]),
            models.Index(fields=["numero_documento"]),
        ]

    def __str__(self):
        nombre_completo = f"{self.nombre} {self.apellido}".strip()
        return f"{self.numero_documento} - {nombre_completo}"
