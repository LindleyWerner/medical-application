from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import *
from .forms import AdmForm
from django.contrib.auth.models import User
DEFAULT_CODE = "q1a2z3"


def index(request):
    valid_adm = __is_valid_adm(request)
    if valid_adm is True:
        context = {'user_type': 'Adm', 'funcs': Funcionalidade.objects.all()}
        return render(request, 'adm_app/index.html', context)
    return valid_adm


def adm_login(request, user):
    context = {'user_type': None}
    if user is not None:
        adm = Adm_user.objects.get(django_user=user)
        if adm is not None and adm.validation_code == DEFAULT_CODE:
            login(request, user)
            context['funcs'] = Funcionalidade.objects.all()
            context['user_type'] = 'User'
            return render(request, 'user_app/index.html', context)
        context['error_message'] = "Usuário inválido"
    else:
        context['error_message'] = 'Erro desconhecido tente se conectar novamente, se persistir '\
                                    'contate o administrador do sistema'
    return render(request, 'core_app/login.html', context)


def register(request):
    form = AdmForm(request.POST or None)
    context = {
        "form": form,
        "user_type": None
    }
    if __is_valid_adm(request) is True:
        context['funcs'] = Funcionalidade.objects.all()
        context.pop('form')
        context['user_type'] = 'Adm'
        return render(request, 'adm_app/index.html', context)
    elif request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['username']
            cnpj = form.cleaned_data['cnpj']
            email = form.cleaned_data['email']
            site = form.cleaned_data['site']
            address = form.cleaned_data['address']
            phones = form.cleaned_data['phones']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            validation_code = form.cleaned_data['validation_code']

            try:
                user = User.objects.get(username=email)
            except:
                user = None

            if user is None:
                context['error_message'] = "O email digitado não consta no sistema, digite corretamente ou "\
                                            "solicite seu cadastro ao administrador do sistema"
                return render(request, 'core_app/register.html', context)

            try:
                adm = Adm_user.objects.get(django_user=user)
            except:
                adm = None

            if adm is not None:
                if adm.validation_code == DEFAULT_CODE:
                    context['error_message'] = 'Esta conta já foi registrada'
                    context.pop('form')
                    return render(request, 'core_app/login.html', context)
                if adm.cnpj != cnpj:
                    context['error_message'] = "O CNPJ digitado não consta no sistema, digite corretamente ou "\
                                                "solicite seu cadastro ao administrador do sistema"
                    return render(request, 'core_app/register.html', context)
                if password1 != password2:
                    context['error_message'] = "As senhas devem ser iguais"
                    return render(request, 'core_app/register.html', context)
                if adm.validation_code != validation_code:
                    context['error_message'] = "O código de validação está incorreto"
                    return render(request, 'core_app/register.html', context)

                user.set_password(password1)
                user.save()

                adm.validation_code = DEFAULT_CODE
                adm.cnpj = cnpj
                adm.full_name = name
                adm.site = site
                adm.address = address
                adm.phones = phones
                adm.save()

                actual_user = authenticate(username=email, password=password1)
                if actual_user is not None:
                    if user.is_active:
                        login(request, actual_user)
                        context['funcs'] = Funcionalidade.objects.all()
                        context.pop('form')
                        context['user_type'] = 'Adm'
                        return render(request, 'adm_app/index.html', context)
                context['error_message'] = "Erro de autenticação, tente novamente"
            else:
                context['error_message'] = "Usuário já cadastrado no sistema"
                context.pop('form')
                return render(request, 'core_app/login.html', context)
    return render(request, 'core_app/register.html', context)


def __is_valid_adm(request):
    context = {'user_type': None}
    if request.user.is_authenticated():
        if request.user.groups.filter(name='Adm').exists():
            return True
    context['error_message'] = 'Você precisa estar autenticado como administrador para acessar esta funcionalidade'
    return render(request, 'core_app/login.html', context)
