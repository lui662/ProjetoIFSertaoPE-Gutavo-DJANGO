from django.shortcuts import render, redirect
from accounts.forms.auth.login_forms import CustomUserLoginForms


def login(request):
    if request.method == "POST": 
        form = CustomUserLoginForms(request, data=request.POST)
        if form.is_valid(): 
            from django.contrib.auth import login as auth_login
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else: 
        form = CustomUserLoginForms()

    return render(request, 'registration/login.html', {'form': form})
