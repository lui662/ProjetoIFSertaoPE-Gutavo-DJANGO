from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Conta 
import random

@receiver(post_save, sender=User)
def create_user_conta(sender, instance, created, **kwargs):
    if created:
        numero_conta = str(random.randint(10000000, 99999999))
        
        while Conta.objects.filter(numero_conta=numero_conta).exists():
            numero_conta = str(random.randint(10000000, 99999999))
        
        Conta.objects.create(
            user=instance,
            numero_conta=numero_conta,
            agencia='0001',
            saldo=0.00
        )
