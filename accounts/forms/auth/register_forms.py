from django import forms
from django.contrib.auth.forms import UserCreationForm
from ...models.user import User


class CustomUserCreateForms(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'tipo_usuario', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['tipo_usuario'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        self.fields['tipo_usuario'].choices = [
            ('cliente', 'Cliente'),
            ('gerente', 'Gerente'),
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email já utilizado")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.tipo_usuario = self.cleaned_data['tipo_usuario']
        if commit:
            user.save()
        return user
