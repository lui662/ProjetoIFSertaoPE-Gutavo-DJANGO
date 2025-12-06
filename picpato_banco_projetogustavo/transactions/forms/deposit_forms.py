from django import forms
from ..models import DepositTransaction


class DepositForm(forms.ModelForm):
    
    class Meta:
        model = DepositTransaction
        fields = ['valor']

    valor = forms.DecimalField(
        label="Valor do Depósito R$",
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "digite o valor do depósito",
            "step": "0.01",
            "min": "0.01",
        }),
    )

    def clean_valor(self):
        valor = self.cleaned_data.get("valor")
        if valor <= 0:
            raise forms.ValidationError("O valor do depósito deve ser maior que zero.")
        return valor