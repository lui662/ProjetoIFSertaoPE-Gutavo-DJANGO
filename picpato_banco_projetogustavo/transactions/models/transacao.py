from django.db import models


class Transacao(models.Model):
    
    TIPO_TRANSACAO_CHOICES = [
        ('deposito', 'Depósito'),
        ('saque', 'Saque'),
        ('transferencia', 'Transferência'),
    ]

    conta_origem = models.ForeignKey(
        'accounts.Conta',
        on_delete=models.CASCADE,
        related_name='transacoes_origem',
        null=True,
        blank=True,
    )

    conta_destino = models.ForeignKey(
        'accounts.Conta',
        on_delete=models.CASCADE,
        related_name='transacoes_destino',
        null=True,
        blank=True,
    )

    tipo = models.CharField(
        max_length=20,
        choices=TIPO_TRANSACAO_CHOICES,
    )

    valor = models.DecimalField(max_digits=12, decimal_places=2)
    data_hora = models.DateTimeField(auto_now_add=True)
    descricao = models.TextField(blank=True)
    
    def __str__(self):
        return f"Transação {self.tipo} de R$ {self.valor} em {self.data_hora}"