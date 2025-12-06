from django import forms
from ..models import DepositTransaction 


class SaqueForm(forms.ModelForm):

    class Meta:
        model = DepositTransaction
        fields = ['valor']

    valor = forms.DecimalField(
        label="Valor do Saque R$",
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "digite o valor do saque",
            "step": "0.01",
            "min": "0.01",
        }),
    )

    def clean_valor(self):
        valor = self.cleaned_data.get("valor")
        if valor <= 0:
            raise forms.ValidationError("O valor do saque deve ser maior que zero.")
        elif valor is None:
            raise forms.ValidationError("O valor do saque não pode ser vazio.")
        elif valor > Decimal('10000.00'):
            raise forms.ValidationError("O limite máximo para saque é R$ 10.000,00.")
        return valor
    
