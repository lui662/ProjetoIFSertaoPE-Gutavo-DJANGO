from django.shortcuts import render, redirect
from accounts.forms.auth.register_forms import CustomUserCreateForms

def register(request):
    if request.method == "POST": 
        form = CustomUserCreateForms(request.POST)
        if form.is_valid(): 
            form.save()
            return redirect('login')
    else: 
        form = CustomUserCreateForms()

    return render(request, 'registration/register.html', {'form': form})
