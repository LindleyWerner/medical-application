from django import forms
from .models import Simple_user
from django.conf import settings

class UserForm(forms.ModelForm):
    GENDERS = [('masculino', 'Masculino'), ('feminino', 'Feminino')]

    username = forms.CharField(label="Nome completo", min_length=2, max_length=70)
    email = forms.EmailField(label="Email", min_length=8, max_length=50)
    cpf = forms.CharField(label="CPF", min_length=11, max_length=11)
    birth_date = forms.CharField(label='Data de nascimento', min_length=6, max_length=10)
    gender = forms.ChoiceField(label="Sexo", choices=GENDERS)
    address = forms.CharField(label="Endereço completo", min_length=5, max_length=50)
    phones = forms.CharField(label="Telefone(s)", max_length=30)
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Senha", max_length=20, min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirmação da senha", max_length=20,
                                min_length=8)

    class Meta:
        model = Simple_user
        fields = ['username','email','cpf','birth_date','gender','address','phones','password1','password2']




