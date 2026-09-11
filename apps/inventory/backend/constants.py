from django.db import models

class ArticuloEstado(models.TextChoices):
    ACTIVO = "ACTIVO", "Activo"
    INACTIVO = "INACTIVO", "Inactivo"

class UnidadMedida(models.TextChoices):
    UNIDAD = "UNIDAD", "Unidad"
    CAJA = "CAJA", "Caja"
    PAQUETE = "PAQUETE", "Paquete"
    DOCENA = "DOCENA", "Docena"
    KILOGRAMO = "KILOGRAMO", "Kilogramo"
    GRAMO = "GRAMO", "Gramo"
    LITRO = "LITRO", "Litro"
    MILILITRO = "MILILITRO", "Mililitro"
    METRO = "METRO", "Metro"

class ClasificacionArticulo(models.TextChoices):
    CAMISAS = "CAMISAS", "Camisas"
    PANTALONES = "PANTALONES", "Pantalones"
    CALZADO = "CALZADO", "Calzado"
    ACCESORIOS = "ACCESORIOS", "Accesorios"
    ELECTRONICA = "ELECTRONICA", "Electrónica"
    HOGAR = "HOGAR", "Hogar"
    OFICINA = "OFICINA", "Oficina"
    ALIMENTOS = "ALIMENTOS", "Alimentos"
    BEBIDAS = "BEBIDAS", "Bebidas"
    OTROS = "OTROS", "Otros"
    NACIONAL = "NACIONAL", "Nacional"
