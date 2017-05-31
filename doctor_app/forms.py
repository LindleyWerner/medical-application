from django import forms
from .models import Doctor_user

class DoctorForm(forms.ModelForm):
    GENDERS = [('masculino', 'Masculino'), ('feminino', 'Feminino')]

    username = forms.CharField(label="Nome completo", min_length=2, max_length=70, required=True)
    email = forms.EmailField(label="Email", min_length=8, max_length=50, required=True)
    crm = forms.CharField(label="CRM", min_length=1, max_length=11, required=True)
    birth_date = forms.CharField(label='Data de nascimento', min_length=6, max_length=10, required=True)
    gender = forms.ChoiceField(label="Sexo", choices=GENDERS, required=True)
    address = forms.CharField(label="Endereço completo", min_length=5, max_length=70, required=True)
    phones = forms.CharField(label="Telefone(s)", max_length=30, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Senha", max_length=20, min_length=8, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirmação da senha", max_length=20, min_length=8,
                                required=True)
    validation_code = forms.CharField(label="Código de validação", min_length=5, max_length=50, required=True)

    class Meta:
        model = Doctor_user
        fields = ['username', 'email', 'crm', 'birth_date', 'gender', 'address', 'phones', 'password1', 'password2',
                  'validation_code']
