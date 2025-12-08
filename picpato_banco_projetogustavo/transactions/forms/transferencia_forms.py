from django import forms

class TransferenciaForm(forms.Form): 
    
    agencia = forms.CharField(
        label="Agência de Destino",
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex: 0001",
        }),
    )

    conta_destino = forms.CharField(
        label="Conta de Destino (Número)",
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ex: 123456",
        }),
    )

    valor = forms.DecimalField(
        label="Valor da Transferência (R$)",
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Digite o valor",
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
            "placeholder": "Opcional: Ex: Pagamento do Aluguel",
        }),
    )

    def clean_valor(self):
        valor = self.cleaned_data.get("valor")
        if valor is None:
            raise forms.ValidationError("O valor da transferência não pode ser vazio.")
        if valor <= 0:
            raise forms.ValidationError("O valor da transferência deve ser maior que zero.")
        return valor