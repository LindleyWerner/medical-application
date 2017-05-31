from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import *
from .forms import DoctorForm
from django.contrib.auth.models import User
DEFAULT_CODE = "q1a2z3"


def index(request):
    valid_doctor = __is_valid_doctor(request)
    if valid_doctor is True:
        context = {'user_type': 'Doctor', 'funcs': Funcionalidade.objects.all(), 'name': request.user.first_name}
        return render(request, 'doctor_app/index.html', context)
    return valid_doctor


def doctor_login(request, user):
    context = {'user_type': None}
    if user is not None:
        doctor = Doctor_user.objects.get(django_user=user)
        if doctor is not None and doctor.validation_code == DEFAULT_CODE:
            login(request, user)
            context['funcs'] = Funcionalidade.objects.all()
            context['name'] = user.first_name
            context['user_type'] = 'User'
            return render(request, 'doctor_app/index.html', context)
        context['error_message'] = "Usuário inválido"
    else:
        context['error_message'] = 'Erro desconhecido tente se conectar novamente, se persistir '\
                                    'contate o administrador'
    return render(request, 'core_app/login.html', context)


def register(request):
    form = DoctorForm(request.POST or None)
    context = {
        "form": form,
        "user_type": None
    }
    if __is_valid_doctor(request) is True:
        context['funcs'] = Funcionalidade.objects.all()
        context.pop('form')
        context['user_type'] = 'Doctor'
        context['name'] = request.user.first_name
        return render(request, 'doctor_app/index.html', context)
    elif request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['username']
            crm = form.cleaned_data['crm']
            email = form.cleaned_data['email']
            birth_date = form.cleaned_data['birth_date']
            gender = form.cleaned_data['gender']
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
                                            "solicite seu cadastro ao administrador do seu local de trabalho"
                return render(request, 'core_app/register.html', context)

            try:
                doctor = Doctor_user.objects.get(django_user=user)
            except:
                doctor = None

            if doctor is not None:
                if doctor.validation_code == DEFAULT_CODE:
                    context['error_message'] = 'Esta conta já foi registrada'
                    context.pop('form')
                    return render(request, 'core_app/login.html', context)
                if doctor.crm != crm:
                    context['error_message'] = "O CRM digitado não consta no sistema, digite corretamente ou "\
                                                "solicite seu cadastro ao administrador do seu local de trabalho"
                    return render(request, 'core_app/register.html', context)
                if password1 != password2:
                    context['error_message'] = "As senhas devem ser iguais"
                    return render(request, 'core_app/register.html', context)
                if doctor.validation_code != validation_code:
                    context['error_message'] = "O código de validação está incorreto"
                    return render(request, 'core_app/register.html', context)

                name_list = name.split()
                user.set_password(password1)
                user.first_name = name_list[0]
                user.last_name = name_list[-1]
                user.save()

                doctor.validation_code = DEFAULT_CODE
                doctor.crm = crm
                doctor.full_name = name
                doctor.birth_date = birth_date
                doctor.gender = gender
                doctor.address = address
                doctor.phones = phones
                doctor.save()

                actual_user = authenticate(username=email, password=password1)
                if actual_user is not None:
                    if user.is_active:
                        login(request, actual_user)
                        context['funcs'] = Funcionalidade.objects.all()
                        context.pop('form')
                        context['user_type'] = 'Doctor'
                        context['name'] = user.first_name
                        return render(request, 'doctor_app/index.html', context)
                context['error_message'] = "Erro de autenticação, tente novamente"
            else:
                context['error_message'] = "Usuário já cadastrado no sistema"
                context.pop('form')
                return render(request, 'core_app/login.html', context)
    return render(request, 'core_app/register.html', context)


def documents(request):
    valid_doctor = __is_valid_doctor(request)
    if valid_doctor is True:
        context = {'user_type': 'Doctor', 'func': 'Documentos'}
        return render(request, 'user_app/test.html', context)
    return valid_doctor


def code(request):
    valid_doctor = __is_valid_doctor(request)
    if valid_doctor is True:
        context = {'user_type': 'Doctor', 'func': 'Código'}
        return render(request, 'user_app/test.html', context)
    return valid_doctor


def consultation(request):
    valid_doctor = __is_valid_doctor(request)
    if valid_doctor is True:
        context = {'user_type': 'Doctor', 'func': 'Consultas'}
        return render(request, 'user_app/test.html', context)
    return valid_doctor


def patient(request):
    valid_doctor = __is_valid_doctor(request)
    if valid_doctor is True:
        context = {'user_type': 'Doctor', 'func': 'Pacientes'}
        return render(request, 'user_app/test.html', context)
    return valid_doctor


def __is_valid_doctor(request):
    context = {'user_type': None}
    if request.user.is_authenticated():
        if request.user.groups.filter(name='Doctor').exists():

            return True
    context['error_message'] = 'Você precisa estar autenticado como médico para acessar esta funcionalidade'
    return render(request, 'core_app/login.html', context)
