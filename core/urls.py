from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views 
from .views import HomeView
from django.views.generic import RedirectView # <-- Importe o RedirectView

urlpatterns = [
    # Esta linha redireciona a raiz (http://...:8000/)
    path('', RedirectView.as_view(pattern_name='register'), name='index'),

    # Suas URLs existentes:
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('home/', HomeView.as_view(), name='home'),
    path('depositar/', views.depositar_view, name='depositar'),
    path('logout/', views.logout_view, name='logout'),
]