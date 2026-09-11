from django.db import models

class ArticuloEstado(models.TextChoices):
    ACTIVO = "ACTIVO", "Activo"
    INACTIVO = "INACTIVO", "Inactivo"

class UnidadMedida(models.TextChoices):
    #UNIDAD = "UNIDAD", "Unidad"
    #CAJA = "CAJA", "Caja"
    #PAQUETE = "PAQUETE", "Paquete"
    #DOCENA = "DOCENA", "Docena"
    #KILOGRAMO = "KILOGRAMO", "Kilogramo"
    #GRAMO = "GRAMO", "Gramo"
    #LITRO = "LITRO", "Litro"
    #MILILITRO = "MILILITRO", "Mililitro"
    METRO = "METRO", "Metro"

class ClasificacionArticulo(models.TextChoices):
    ANTIFLUIDO = "ANTIFLUIDO", "Antifluido"
    IMPORTADO = "IMPORTADO", "Importado"
    OTROS = "OTROS", "Otros"
    NACIONAL = "NACIONAL", "Nacional"
