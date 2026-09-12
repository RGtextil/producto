from decimal import Decimal, InvalidOperation

from django import template


register = template.Library()


@register.filter
def moneda(valor):
    try:
        valor = Decimal(valor)
    except (InvalidOperation, TypeError, ValueError):
        return valor

    valor = valor.quantize(Decimal("0.01"))

    partes = f"{valor:,.2f}".split(".")

    miles = partes[0].replace(",", ".")
    decimales = partes[1]

    return f"{miles},{decimales}"