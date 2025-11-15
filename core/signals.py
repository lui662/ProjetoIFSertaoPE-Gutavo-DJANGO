# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Conta
import random # Para gerar o número da conta

# Este "receiver" escuta pelo sinal 'post_save' do nosso modelo User
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_account(sender, instance, created, **kwargs):
    if created: # 'created' é True apenas se for um novo registo

        # Gera um número de conta simples e aleatório
        numero_conta = f"{random.randint(1000, 9999)}-{random.randint(0, 9)}"

        # Cria a Conta e liga-a ao User ('instance' é o User que foi criado)
        Conta.objects.create(user=instance, numero_conta=numero_conta, saldo=0.00)