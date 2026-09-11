from django.db import models


class CarteraEstado(models.TextChoices):
    PENDIENTE = "PENDIENTE", "Pendiente"
    PAGADA = "PAGADA", "Pagada"


class CarteraTipo(models.TextChoices):
    PEDIDO = "PEDIDO", "Pedido"
    OTRA = "OTRA", "Otra cartera"