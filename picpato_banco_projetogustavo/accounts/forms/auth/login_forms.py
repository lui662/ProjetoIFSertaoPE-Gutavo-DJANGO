from django import forms
from django.contrib.auth.forms import UserCreationForm
from ...models.user import User


class CustomUserLoginForms(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            from django.contrib.auth import authenticate
            user = authenticate(self.request, username=username, password=password)
            if user is None:
                raise forms.ValidationError("Nome de usuário ou senha inválidos.")
            self.user = user
        return cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)