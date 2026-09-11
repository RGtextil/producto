from django.db import models


class OtroDineroTipo(models.TextChoices):
    EFECTIVO = "EFECTIVO", "Efectivo"
    BANCO = "BANCO", "Banco"
    OTRO = "OTRO", "Otro"


class DeudaTipo(models.TextChoices):
    PROVEEDOR = "PROVEEDOR", "Proveedor"
    PRESTAMO = "PRESTAMO", "Préstamo"
    OTRO = "OTRO", "Otra deuda"