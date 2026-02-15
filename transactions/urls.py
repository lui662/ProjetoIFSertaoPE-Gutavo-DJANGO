from django.urls import path
from .views.deposito import deposito
from .views.transferencia import transferencia
from .views.api.transferencia_api import transferencia_api
from .views.api.deposito_api import deposito_api


urlpatterns = [
    path('deposito/', deposito, name='depositar'),
    path('transferencia/', transferencia, name='transferir'),
    path('transferencia_api/', transferencia_api, name='transferencia_api'),
    path('deposito_api/', deposito_api, name='deposito_api'),
]