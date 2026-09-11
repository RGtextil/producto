from decimal import Decimal

from django import forms

from apps.inventory.backend.constants import (
    ArticuloEstado,
    ClasificacionArticulo,
    UnidadMedida,
)


class ArticuloCreateForm(forms.Form):
    descripcion = forms.CharField(
        label="Descripción",
        max_length=255,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. Camisa Oxford",
            }
        ),
    )

    clasificacion = forms.ChoiceField(
        label="Clasificación",
        choices=ClasificacionArticulo.choices,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    unidad_medida = forms.ChoiceField(
        label="Unidad de medida",
        choices=UnidadMedida.choices,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    costo_base = forms.DecimalField(
        label="Costo base",
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0"),
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01",
            }
        ),
    )

    alerta_minimo = forms.DecimalField(
        label="Alerta de mínimo",
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0"),
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01",
            }
        ),
    )

    ubicacion_almacen = forms.CharField(
        label="Ubicación en almacén",
        max_length=150,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. Estante A-01",
            }
        ),
    )

    color = forms.CharField(
        label="Color",
        max_length=80,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. Azul",
            }
        ),
    )

    def clean_descripcion(self):
        descripcion = self.cleaned_data["descripcion"]

        if not descripcion:
            raise forms.ValidationError(
                "La descripción es obligatoria."
            )

        return descripcion


class ArticuloUpdateForm(forms.Form):
    costo_base = forms.DecimalField(
        label="Costo base",
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0"),
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01",
            }
        ),
    )

    alerta_minimo = forms.DecimalField(
        label="Alerta de mínimo",
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0"),
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01",
            }
        ),
    )

    ubicacion_almacen = forms.CharField(
        label="Ubicación en almacén",
        max_length=150,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. Estante A-01",
            }
        ),
    )

    estado = forms.ChoiceField(
        label="Estado",
        choices=ArticuloEstado.choices,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )


class ItemInventarioForm(forms.Form):
    cantidad = forms.DecimalField(
        label="Cantidad",
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0"),
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01",
            }
        ),
    )

    ubicacion = forms.CharField(
        label="Ubicación",
        max_length=150,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. Estante A-01",
            }
        ),
    )

    def clean_cantidad(self):
        cantidad = self.cleaned_data["cantidad"]

        if cantidad < 0:
            raise forms.ValidationError(
                "La cantidad no puede ser negativa."
            )

        return cantidad
