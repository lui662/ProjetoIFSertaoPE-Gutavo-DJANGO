from django.urls import path
from .views.deposito import deposito
from .views.transferencia import transferencia


urlpatterns = [
    path('deposito/', deposito, name='depositar'),
    path('transferencia/', transferencia, name='transferir'),
]