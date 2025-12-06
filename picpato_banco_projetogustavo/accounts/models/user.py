from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    TIPO_USUARIO_CHOICES = [
        ('cliente', 'Cliente'),
        ('gerente', 'Gerente'),
    ]

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='cliente',
    )

    def __str__(self):
        return ""f"{self.username} ({self.get_tipo_usuario_display()})"
    