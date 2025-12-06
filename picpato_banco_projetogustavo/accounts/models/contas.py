from django.db import models
from django.conf import settings

class contas(models.Model):
    
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='contas',
        primary_key=True,
    )

    agencia = models.CharField(max_length=10, default='0001')
    numero_conta = models.CharField(max_length=20, unique=True, blank=True)

    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Conta {self.numero_conta} - Agência {self.agencia} - Saldo: R$ {self.saldo}"
    