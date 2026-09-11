from decimal import Decimal

from django import forms

from apps.customers.backend.constants import (
    ClienteEstado,
    TipoDocumento,
)


class ClienteCreateForm(forms.Form):
    tipo_documento = forms.ChoiceField(
        label="Tipo de documento",
        choices=TipoDocumento.choices,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    numero_documento = forms.CharField(
        label="Número de documento",
        max_length=30,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. 1234567890",
            }
        ),
    )

    nombre = forms.CharField(
        label="Nombre",
        max_length=150,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. Juan",
            }
        ),
    )

    apellido = forms.CharField(
        label="Apellido",
        max_length=150,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. Pérez",
            }
        ),
    )

    telefono = forms.CharField(
        label="Teléfono",
        max_length=30,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. 3001234567",
            }
        ),
    )

    email = forms.EmailField(
        label="Correo electrónico",
        max_length=254,
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "cliente@ejemplo.com",
            }
        ),
    )

    direccion = forms.CharField(
        label="Dirección",
        max_length=255,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. Calle 10 # 20-30",
            }
        ),
    )

    ciudad = forms.CharField(
        label="Ciudad",
        max_length=100,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. Bogotá",
            }
        ),
    )

    departamento = forms.CharField(
        label="Departamento",
        max_length=100,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. Cundinamarca",
            }
        ),
    )

    limite_credito = forms.DecimalField(
        label="Límite de crédito",
        max_digits=12,
        decimal_places=2,
        min_value=Decimal("0"),
        initial=Decimal("0"),
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "min": "0",
                "step": "0.01",
            }
        ),
    )

    def clean_numero_documento(self):
        numero_documento = self.cleaned_data["numero_documento"].strip()

        if not numero_documento:
            raise forms.ValidationError(
                "El número de documento es obligatorio."
            )

        return numero_documento


class ClienteUpdateForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        max_length=150,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    apellido = forms.CharField(
        label="Apellido",
        max_length=150,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    telefono = forms.CharField(
        label="Teléfono",
        max_length=30,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    email = forms.EmailField(
        label="Correo electrónico",
        max_length=254,
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    direccion = forms.CharField(
        label="Dirección",
        max_length=255,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    ciudad = forms.CharField(
        label="Ciudad",
        max_length=100,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    departamento = forms.CharField(
        label="Departamento",
        max_length=100,
        required=False,
        strip=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    limite_credito = forms.DecimalField(
        label="Límite de crédito",
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

    estado = forms.ChoiceField(
        label="Estado",
        choices=ClienteEstado.choices,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )
