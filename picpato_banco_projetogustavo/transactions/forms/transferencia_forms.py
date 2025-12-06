from django import forms
from ..models import DepositTransaction


class DepositForm(forms.ModelForm):

    class Meta:
        model = DepositTransaction
        fields = ['valor']

    conta_destino = forms.CharField(
        label="Conta Destino",
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "digite a conta destino",
        }),
    )

    valor = forms.DecimalField(
        label="Valor da Transferência R$",
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "digite o valor da transferência",
            "step": "0.01",
            "min": "0.01",
        }),
    )

    descricao = forms.CharField(
        label="Descrição",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "opcional: digite uma descrição para a transferência",
        }),
    )

    def clean_valor(self):
        valor = self.cleaned_data.get("valor")
        if valor <= 0:
            raise forms.ValidationError("O valor da transferência deve ser maior que zero.")
        elif valor is None:
            raise forms.ValidationError("O valor da transferência não pode ser vazio.")
        return valor