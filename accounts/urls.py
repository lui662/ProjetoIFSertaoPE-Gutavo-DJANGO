from django.urls import path

from accounts.views.auth.login import login
from accounts.views.auth.register import register
from accounts.views.auth.logout import logout

urlpatterns = [
    path('login/', login, name="login"), 
    path('register/', register, name="register"), 
    path('logout/', logout, name="logout")
]



