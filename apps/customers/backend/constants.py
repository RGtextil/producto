from django.db import models


class ClienteEstado(models.TextChoices):
    ACTIVO = "ACTIVO", "Activo"
    INACTIVO = "INACTIVO", "Inactivo"


class TipoDocumento(models.TextChoices):
    CEDULA = "CC", "Cédula de ciudadanía"
    NIT = "NIT", "NIT"
    CEDULA_EXTRANJERIA = "CE", "Cédula de extranjería"
    PASAPORTE = "PASAPORTE", "Pasaporte"
