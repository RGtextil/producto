from decimal import Decimal

from django import forms

from apps.customers.backend.constants import ClienteEstado
from apps.customers.backend.models import Cliente
from apps.inventory.backend.constants import ArticuloEstado
from apps.inventory.backend.models import Articulo


class PedidoCreateForm(forms.Form):
    cliente = forms.ModelChoiceField(
        label="Cliente",
        queryset=Cliente.objects.filter(
            estado=ClienteEstado.ACTIVO,
        ).order_by(
            "nombre",
            "apellido",
        ),
        empty_label="Seleccione un cliente",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )


class PedidoItemForm(forms.Form):
    articulo = forms.ModelChoiceField(
        label="Artículo",
        queryset=Articulo.objects.filter(
            estado=ArticuloEstado.ACTIVO,
        ).order_by(
            "descripcion",
            "id",
        ),
        empty_label="Seleccione un artículo",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    cantidad = forms.DecimalField(
        label="Cantidad",
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0.01"),
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "0.01",
                "step": "0.01",
                "placeholder": "Ej. 1",
            }
        ),
    )

    precio_venta = forms.DecimalField(
        label="Precio de venta",
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0"),
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01",
                "placeholder": "Ej. 25000.00",
            }
        ),
    )

    def clean_cantidad(self):
        cantidad = self.cleaned_data["cantidad"]

        if cantidad <= 0:
            raise forms.ValidationError(
                "La cantidad debe ser mayor que cero."
            )

        return cantidad

    def clean_precio_venta(self):
        precio_venta = self.cleaned_data["precio_venta"]

        if precio_venta < 0:
            raise forms.ValidationError(
                "El precio de venta no puede ser negativo."
            )

        return precio_venta


class PedidoForm(forms.Form):
    cliente = forms.ModelChoiceField(
        label="Cliente",
        queryset=Cliente.objects.filter(
            estado=ClienteEstado.ACTIVO,
        ).order_by(
            "nombre",
            "apellido",
        ),
        empty_label="Seleccione un cliente",
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    def clean_cliente(self):
        cliente = self.cleaned_data["cliente"]

        if cliente.estado != ClienteEstado.ACTIVO:
            raise forms.ValidationError(
                "El cliente está inactivo."
            )

        return cliente