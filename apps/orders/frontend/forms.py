from decimal import Decimal

from django import forms


class PedidoArticuloForm(forms.Form):

    descripcion = forms.CharField(
        label="Descripción",
        required=True,
        max_length=255,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_descripcion",
            }
        ),
    )

    color = forms.CharField(
        label="Color",
        required=True,
        max_length=100,
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_color",
                "disabled": True,
            }
        ),
    )

    cantidad = forms.DecimalField(
        label="Cantidad",
        required=True,
        min_value=Decimal("0.01"),
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "0.01",
                "step": "0.01",
                "placeholder": "0.00",
            }
        ),
    )

    precio_venta = forms.DecimalField(
        label="Precio de venta",
        required=True,
        min_value=Decimal("0"),
        max_digits=14,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01",
                "placeholder": "0.00",
            }
        ),
    )

    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"].strip()

        if not descripcion:
            raise forms.ValidationError(
                "La descripción es obligatoria."
            )

        return descripcion

    def clean_color(self):
        color = self.cleaned_data["color"].strip()

        if not color:
            raise forms.ValidationError(
                "El color es obligatorio."
            )

        return color

    def clean_cantidad(self):
        cantidad = self.cleaned_data["cantidad"]

        if cantidad <= 0:
            raise forms.ValidationError(
                "La cantidad debe ser mayor que cero."
            )

        return cantidad

    def clean_precio_venta(self):
        precio = self.cleaned_data["precio_venta"]

        if precio < 0:
            raise forms.ValidationError(
                "El precio de venta no puede ser negativo."
            )

        return precio


class PedidoClienteForm(forms.Form):

    cliente_id = forms.IntegerField(
        label="Cliente",
        required=True,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )