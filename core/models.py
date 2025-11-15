# core/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings # Importe o settings

# Seu modelo User (EXISTENTE)
class User(AbstractUser):
    TIPO_USUARIO_CHOICES = (
        ("cliente", "Cliente"),
        ("gerente", "Gerente"),
    )
    tipo_usuario = models.CharField(
        max_length=10, 
        choices=TIPO_USUARIO_CHOICES, 
        default="cliente"
    )
    # ... (não apague nada do seu User) ...

# --- ADICIONE O MODELO CONTA ABAIXO ---
class Conta(models.Model):
    # Ligação 1-para-1: Cada Usuário tem UMA Conta.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, # Usa o 'core.User' que definimos
        on_delete=models.CASCADE,
        primary_key=True # A ligação ao User é a chave primária
    )
    
    agencia = models.CharField(max_length=4, default='0001')
    numero_conta = models.CharField(max_length=10, unique=True, blank=True) # Deixamos blank=True por agora
    
    # NUNCA use FloatField para dinheiro. DecimalField é o correto.
    saldo = models.DecimalField(
        max_digits=10, # Ex: 9.999.999,99
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return f"Conta {self.agencia}-{self.numero_conta} ({self.user.username})"

# --- ADICIONE O MODELO TRANSACAO ABAIXO ---
class Transacao(models.Model):
    TIPO_TRANSACAO_CHOICES = (
        ('E', 'Entrada'),
        ('S', 'Saída'),
    )

    # Ligação Muitos-para-1: Cada Transação pertence a UMA Conta.
    conta = models.ForeignKey(
        Conta, 
        on_delete=models.CASCADE, 
        related_name='transacoes' # Para podermos fazer conta.transacoes.all()
    )
    
    tipo = models.CharField(max_length=1, choices=TIPO_TRANSACAO_CHOICES)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.CharField(max_length=100)
    data_hora = models.DateTimeField(auto_now_add=True) # Data e hora automáticas

    def __str__(self):
        return f"{self.get_tipo_display()} de {self.valor} para {self.conta.user.username}"