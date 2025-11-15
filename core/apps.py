# core/apps.py
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    # --- ADICIONE ESTE MÉTODO ---
    def ready(self):
        import core.signals # Importa os nossos sinais