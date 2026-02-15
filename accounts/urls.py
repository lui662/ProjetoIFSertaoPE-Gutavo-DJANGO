from django.urls import path

from accounts.views.auth.login import login
from accounts.views.auth.register import register
from accounts.views.auth.logout import logout
from accounts.views.api.register_api import register_api
from accounts.views.api.login_api import login_api

urlpatterns = [
    path('login/', login, name="login"), 
    path('register/', register, name="register"), 
    path('logout/', logout, name="logout"),
    path('register_api/', register_api, name="register_api"),
    path('login_api/', login_api, name="login_api"),
]



