from django import forms

from apps.balance.backend.constants import DeudaTipo, OtroDineroTipo


class OtroDineroForm(forms.Form):
    nombre = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. Caja principal",
            }
        ),
    )

    tipo = forms.ChoiceField(
        choices=OtroDineroTipo.choices,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    concepto = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Concepto",
            }
        ),
    )

    monto = forms.DecimalField(
        min_value=0,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0.01",
                "placeholder": "0.00",
            }
        ),
    )

    fecha = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )


class DeudaForm(forms.Form):
    nombre = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej. Proveedor ABC",
            }
        ),
    )

    tipo = forms.ChoiceField(
        choices=DeudaTipo.choices,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    concepto = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Concepto de la deuda",
            }
        ),
    )

    monto = forms.DecimalField(
        min_value=0,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0.01",
                "placeholder": "0.00",
            }
        ),
    )

    fecha = forms.DateField(
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )

    fecha_vencimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control",
            }
        ),
    )