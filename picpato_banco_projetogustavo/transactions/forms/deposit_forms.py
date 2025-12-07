# transactions/forms/deposit_forms.py
from django import forms

# --- REMOVI A LINHA DE IMPORT DO MODELO QUE DAVA ERRO ---

class DepositForm(forms.Form): # Mudamos de ModelForm para forms.Form
    
    valor = forms.DecimalField(
        label="Valor do Depósito R$",
        max_digits=12,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Digite o valor do depósito",
            "step": "0.01",
            "min": "0.01",
        }),
    )

    def clean_valor(self):
        valor = self.cleaned_data.get("valor")
        
        if valor is None:
             raise forms.ValidationError("Informe um valor válido.")
             
        if valor <= 0:
            raise forms.ValidationError("O valor do depósito deve ser maior que zero.")
            
        return valor