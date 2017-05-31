from django.contrib.auth import logout, login
from django.shortcuts import render
from user_app.views import index as user_index
from user_app.views import user_login
from doctor_app.views import doctor_login
from doctor_app.views import index as doctor_index
from adm_app.views import adm_login
from adm_app.views import index as adm_index
from django.contrib.auth import authenticate


def about(request):
    context = {'user_type': __chek_type(request.user)}
    return render(request, 'core_app/about.html', context)


def error(request):
    context = {'user_type': __chek_type(request.user)}
    return render(request, 'core_app/base.html', context)


def login_user(request):
    context = {'user_type': None}
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                user_type = __chek_type(user)
                if user_type == 'User':
                    return user_login(request, user)
                elif user_type == 'Doctor':
                    return doctor_login(request, user)
                elif user_type == 'Adm':
                    return adm_login(request, user)
                else:
                    context['error_message'] = 'Usuário inválido, tente novamente, se o erro persistir, ' \
                                               'contate o administrador do sistema'
            else:
                context['error_message'] = 'Sua conta foi desconectada'
        else:
            context['error_message'] = 'Usuário e/ou senha inválidos'
    else:
        user_type = __chek_type(request.user)
        if user_type == 'User':
            return user_index(request)
        elif user_type == 'Doctor':
            return doctor_index(request)
        elif user_type == 'Adm':
            return adm_index(request)
    return render(request, 'core_app/login.html', context)


def logout_user(request):
    logout(request)
    context = {'user_type': None}
    return render(request, 'core_app/login.html', context)


def pre_register(request):
    return render(request, 'core_app/pre_register.html')


def __chek_type(user):
    if user.is_authenticated():
        if user.groups.filter(name='User').exists():
            return 'User'
        elif user.groups.filter(name='Doctor').exists():
            return 'Doctor'
        elif user.groups.filter(name='Adm').exists():
            return 'Adm'
    return None
