# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User  # <-- Importa o seu core.User personalizado
from decimal import Decimal

# --- FORMULÁRIO 1: REGISTO (O nosso, que funciona com tipo_usuario) ---
class CustomUserCreationForm(UserCreationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Traduz os rótulos
        self.fields['username'].label = 'Nome de usuário'
        self.fields['email'].label = 'Endereço de e-mail'
        self.fields['tipo_usuario'].label = 'Tipo de usuário'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmação de senha'

    class Meta(UserCreationForm.Meta):
        model = User  # <-- Aponta para o core.User (correto)
        fields = ('username', 'email', 'tipo_usuario') # <-- Inclui tipo_usuario
    
    # Validação de e-mail (como no seu código)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado.")
        return email

# --- FIM DO FORMULÁRIO 1 ---


# --- FORMULÁRIO 2: DEPÓSITO (O seu, está perfeito) ---
class DepositoForm(forms.Form):
    """Formulário para depósitos bancários"""
    valor = forms.DecimalField(
        label='Valor do Depósito (R$)',
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Digite o valor do depósito',
            'step': '0.01',
            'min': '0.01'
        })
    )

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor is None:
            raise forms.ValidationError("O valor é obrigatório.")
        if valor <= 0:
            raise forms.ValidationError("O valor deve ser maior que zero.")
        if valor > Decimal('100000.00'):
            raise forms.ValidationError("O valor máximo por depósito é R$ 100.000,00.")
        return valor


# --- FORMULÁRIO 3: SAQUE (O seu, perfeito) ---
class SaqueForm(forms.Form):
    """Formulário para saques bancários"""
    valor = forms.DecimalField(
        label='Valor do Saque (R$)',
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o valor do saque',
            'step': '0.01',
            'min': '0.01'
        })
    )

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor is None:
            raise forms.ValidationError("O valor é obrigatório.")
        if valor <= 0:
            raise forms.ValidationError("O valor deve ser maior que zero.")
        if valor > Decimal('5000.00'):
            raise forms.ValidationError("O limite máximo por saque é R$ 5.000,00.")
        return valor


# --- FORMULÁRIO 4: TRANSFERÊNCIA (O seu, perfeito) ---
class TransferenciaForm(forms.Form):
    """Formulário para transferências entre contas"""
    conta_destino = forms.CharField(
        label='Número da Conta de Destino',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o número da conta (Ex: 2419-5)'
        })
    )
    valor = forms.DecimalField(
        label='Valor (R$)',
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite o valor',
            'step': '0.01',
            'min': '0.01'
        })
    )
    descricao = forms.CharField(
        label='Descrição',
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Descrição da transferência (opcional)'
        })
    )

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor is None:
            raise forms.ValidationError("O valor é obrigatório.")
        if valor <= 0:
            raise forms.ValidationError("O valor deve ser maior que zero.")
        return valor