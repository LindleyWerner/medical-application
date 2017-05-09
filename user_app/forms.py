from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput, label="Nome", min_length=2, max_length=50)
    cpf = forms.CharField(widget=forms.TextInput, label="CPF (Somente números)", min_length=11, max_length=11)
    email = forms.CharField(widget=forms.EmailInput, label="Email", min_length=8, max_length=50)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Senha", max_length=20, min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirmação da senha", max_length=20, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'cpf', 'email', 'password1', 'password2']
