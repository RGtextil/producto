from django.db import models


class PedidoEstado(models.TextChoices):
    ENTREGADO = "ENTREGADO", "Entregado"
    CANCELADO = "CANCELADO", "Cancelado"
