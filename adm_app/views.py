from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import os
import binascii
from django.db.models import Q
from doctor_app.models import Doctor_user

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
        if adm is not None:
            login(request, user)
            context['funcs'] = Funcionalidade.objects.all()
            context['user_type'] = 'Adm'
            return render(request, 'adm_app/index.html', context)
        context['error_message'] = "Usuário inválido"
    else:
        context['error_message'] = 'Erro desconhecido tente se conectar novamente, se persistir ' \
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
                pending_user = Pending_adm.objects.get(email=email)
            except:
                pending_user = None

            try:
                User.objects.get(username=email)
                user_exist = True
            except:
                user_exist = False

            if pending_user is None:
                context['error_message'] = "O email digitado não consta no sistema, digite corretamente ou " \
                                           "solicite seu cadastro ao administrador do sistema"
                return render(request, 'core_app/register.html', context)
            elif user_exist:
                context['error_message'] = "Usuário já cadastrado no sistema"
                context.pop('form')
                return render(request, 'core_app/login.html', context)
            else:
                if pending_user.validation_code == DEFAULT_CODE:
                    context['error_message'] = 'Esta conta já foi registrada'
                    context.pop('form')
                    return render(request, 'core_app/login.html', context)
                if pending_user.cnpj != cnpj:
                    context['error_message'] = "O CNPJ digitado não consta no sistema, digite corretamente ou " \
                                               "solicite seu cadastro ao administrador do sistema"
                    return render(request, 'core_app/register.html', context)
                if password1 != password2:
                    context['error_message'] = "As senhas devem ser iguais"
                    return render(request, 'core_app/register.html', context)
                if pending_user.validation_code != validation_code:
                    context['error_message'] = "O código de validação está incorreto"
                    return render(request, 'core_app/register.html', context)

                group = Group.objects.get(name='Adm')
                user = User.objects.create_user(username=email, email=email, password=password1)
                user.groups.add(group)

                Adm_user.objects.create(django_user=user, cnpj=cnpj, adm_father=pending_user.adm_father, address=address,
                                        full_name=name, site=site, phones=phones)

                pending_user.delete()

                actual_user = authenticate(username=email, password=password1)
                if actual_user is not None:
                    if user.is_active:
                        login(request, actual_user)
                        context['funcs'] = Funcionalidade.objects.all()
                        context.pop('form')
                        context['user_type'] = 'Adm'
                        return render(request, 'adm_app/index.html', context)
                context['error_message'] = "Erro de autenticação, tente novamente"
    return render(request, 'core_app/register.html', context)


def __is_valid_adm(request):
    context = {'user_type': None}
    if request.user.is_authenticated():
        if request.user.groups.filter(name='Adm').exists():
            return True
    context['error_message'] = 'Você precisa estar autenticado como administrador para acessar esta funcionalidade'
    return render(request, 'core_app/login.html', context)


def list_adm(request):
    valid_adm = __is_valid_adm(request)
    if valid_adm is True:
        query = request.GET.get("q")
        sons = Adm_user.objects.filter(adm_father=request.user.id)
        context = {'user_type': 'Adm', 'not_found': False}
        if query:
            sons = sons.filter(Q(address__icontains=query) | Q(cnpj__icontains=query)
                               | Q(full_name__icontains=query)).distinct()
            if sons.count() == 0:
                context['not_found'] = True

        if sons.count() == 0:
            sons = None
        else:
            sons.order_by('-full_name')

        context['adms'] = sons
        return render(request, 'adm_app/crud_adm.html', context)
    return valid_adm


def add_adm(request):
    valid_adm = __is_valid_adm(request)
    if valid_adm is True:
        form = NewAdmForm(request.POST or None)
        context = {'user_type': 'Adm', 'form': form}

        if request.method == 'POST' and form.is_valid():
            cnpj = form.cleaned_data['cnpj']
            email = form.cleaned_data['email']
            try:
                User.objects.get(username=email)
            except:
                code = str(binascii.hexlify(os.urandom(20)))
                Pending_adm.objects.create(email=email, cnpj=cnpj, validation_code=code, adm_father=request.user.id)

                print('\n\nCódigo\n' + code + '\n\n')
                context['funcs'] = Funcionalidade.objects.all()
                context.pop('form')
                return render(request, 'adm_app/index.html', context)
            context['error_message'] = "Email já cadastrado no sistema"
        context['what_type'] = 'administrador'
        return render(request, 'adm_app/new.html', context)
    return valid_adm


def rm_adm(request, adm_id):
    valid_adm = __is_valid_adm(request)
    if valid_adm is True:
        adm = get_object_or_404(User, pk=adm_id)
        adm.delete()
        return list_adm(request)
    return valid_adm


def list_pending_solicitations(request):
    valid_adm = __is_valid_adm(request)
    if valid_adm is True:
        query = request.GET.get("q")
        # Adm filtering
        adm_sons = Pending_adm.objects.filter(adm_father=request.user.id)
        context = {'user_type': 'Adm', 'adm_not_found': False, 'doctor_not_found': False}
        if query:
            adm_sons = adm_sons.filter(Q(email__icontains=query) | Q(cnpj__icontains=query)).distinct()
            if adm_sons.count() == 0:
                context['adm_not_found'] = True
        if adm_sons.count() == 0:
            adm_sons = None
        else:
            adm_sons.order_by('-email')
        context['pending_adms'] = adm_sons
        # Doctor filtering
        doctor_sons = Pending_doctor.objects.filter(adm_father=request.user.id)
        if query:
            doctor_sons = doctor_sons.filter(Q(email__icontains=query) | Q(crm__icontains=query)).distinct()
            if doctor_sons.count() == 0:
                context['doctor_not_found'] = True
        if doctor_sons.count() == 0:
            doctor_sons = None
        else:
            doctor_sons.order_by('-email')
        context['pending_doctors'] = doctor_sons
        return render(request, 'adm_app/pending_solicitations.html', context)
    return valid_adm


def rm_pending_doctor(request, pending_doctor_id):
    valid_adm = __is_valid_adm(request)
    if valid_adm is True:
        pending_doctor = get_object_or_404(Pending_doctor, pk=pending_doctor_id)
        pending_doctor.delete()
        return list_pending_solicitations(request)
    return valid_adm


def rm_pending_adm(request, pending_adm_id):
    valid_adm = __is_valid_adm(request)
    if valid_adm is True:
        pending_adm = get_object_or_404(Pending_adm, pk=pending_adm_id)
        pending_adm.delete()
        return list_pending_solicitations(request)
    return valid_adm


def list_doctor(request):
    valid_adm = __is_valid_adm(request)
    if valid_adm is True:
        query = request.GET.get("q")
        sons = Doctor_user.objects.filter(adm_father=request.user.id)
        context = {'user_type': 'Adm', 'not_found': False}
        if query:
            sons = sons.filter(Q(crm__icontains=query) | Q(full_name__icontains=query)).distinct()
            if sons.count() == 0:
                context['not_found'] = True

        if sons.count() == 0:
            sons = None
        else:
            sons.order_by('-full_name')

        context['doctors'] = sons
        return render(request, 'adm_app/crud_doctor.html', context)
    return valid_adm


def add_doctor(request):
    valid_adm = __is_valid_adm(request)
    if valid_adm is True:
        form = NewDoctorForm(request.POST or None)
        context = {'user_type': 'Adm', 'form': form}

        if request.method == 'POST' and form.is_valid():
            crm = form.cleaned_data['crm']
            email = form.cleaned_data['email']
            try:
                User.objects.get(username=email)
            except:
                code = str(binascii.hexlify(os.urandom(20)))
                Pending_doctor.objects.create(email=email, crm=crm, validation_code=code, adm_father=request.user.id)

                print('\n\nCódigo\n' + code + '\n\n')
                context['funcs'] = Funcionalidade.objects.all()
                context.pop('form')
                return render(request, 'adm_app/index.html', context)
            context['error_message'] = "Email já cadastrado no sistema"
        context['what_type'] = 'médico'
        return render(request, 'adm_app/new.html', context)
    return valid_adm


def rm_doctor(request, doctor_id):
    valid_adm = __is_valid_adm(request)
    if valid_adm is True:
        doctor = get_object_or_404(User, pk=doctor_id)
        doctor.delete()
        return list_doctor(request)
    return valid_adm