from django import forms
from .models import Adm_user


class AdmForm(forms.ModelForm):
    username = forms.CharField(label="Nome", min_length=2, max_length=70, required=True)
    email = forms.EmailField(label="Email", min_length=8, max_length=50, required=True)
    cnpj = forms.CharField(label="CNPJ", min_length=14, max_length=18, required=True)
    address = forms.CharField(label="Endereço completo", min_length=5, max_length=70, required=True)
    phones = forms.CharField(label="Telefone(s)", max_length=30, required=True)
    site = forms.CharField(label="site(s)", max_length=50)
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Senha", max_length=20, min_length=8, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirmação da senha", max_length=20, min_length=8,
                                required=True)
    validation_code = forms.CharField(label="Código de validação", min_length=5, max_length=50, required=True)

    class Meta:
        model = Adm_user
        fields = ['username', 'email', 'cnpj', 'address', 'phones', 'site', 'password1', 'password2', 'validation_code']
