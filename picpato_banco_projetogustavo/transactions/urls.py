from django.urls import path
from . import views

urlpatterns = [
    path('depositar/', views.deposito, name='depositar'),
]