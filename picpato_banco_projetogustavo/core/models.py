from django.db import models
from django.apps import AppConfig

# Create your models here.
class coreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core' 

class transacao(models.Model):
    
    TIPO_TRANSACAO_CHOICES = [
        ('deposito', 'Depósito'),
        ('saque', 'Saque'),
        ('transferencia', 'Transferência'),
    ]

    conta_origem = models.ForeignKey(
        'accounts.contas',
        on_delete=models.CASCADE,
        related_name='transacoes_origem',
        null=True,
        blank=True,
    )

    conta_destino = models.ForeignKey(
        'accounts.contas',
        on_delete=models.CASCADE,
        related_name='transacoes_destino',
        null=True,
        blank=True,
    )


    