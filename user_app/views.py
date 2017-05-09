from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import *
#from SGCM_V2.models import Custom_user
from .forms import UserForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse


# Create your views here.
def index(request):
    if not request.user.is_authenticated():
        return render(request, 'user_app/login.html')
    else:
        actual_user = Custom_user.objects.get(django_user=request.user)
        if actual_user:
            if actual_user.is_user:
                funcs = Funcionalidades.objects.all()
                return render(request, 'user_app/index.html', {'funcs': funcs, "name": request.user.first_name})
            elif actual_user.is_nurse:
                return HttpResponse("<p>Nurse page</p>")
            elif actual_user.is_pharmacy:
                return HttpResponse("<p>Pharmacy page</p>")
            elif actual_user.is_doctor:
                return HttpResponse("<p>Doctor page</p>")
            elif actual_user.is_adm:
                return HttpResponse("<p>Administrator page</p>")
            else:
                return render(request, 'user_app/register.html', {'error_message': 'Usuário inválido, crie outra '
                                                                                   'conta ou contate o '
                                                                                   'administrador'})
        else:
            return render(request, 'user_app/register.html', {'error_message': 'Usuário inválido, crie outra '
                                                                               'conta ou contate o administrador'})


def login_user(request):
    if request.method == "POST":
        cpf = request.POST['cpf']
        password = request.POST['password']

        user = authenticate(username=cpf, password=password)
        if user is not None:
            if user.is_active:
                actual_user = Custom_user.objects.get(django_user=user)
                if actual_user:
                    login(request, user)
                    if actual_user.is_user:
                        funcs = Funcionalidades.objects.all()
                        return render(request, 'user_app/index.html', {'funcs': funcs, "name": user.first_name})
                    elif actual_user.is_nurse:
                        return HttpResponse("<p>Nurse page</p>")
                    elif actual_user.is_pharmacy:
                        return HttpResponse("<p>Pharmacy page</p>")
                    elif actual_user.is_doctor:
                        return HttpResponse("<p>Doctor page</p>")
                    elif actual_user.is_adm:
                        return HttpResponse("<p>Administrator page</p>")
                    else:
                        return render(request, 'user_app/register.html',
                                      {'error_message': 'Usuário inválido, crie outra '
                                                        'conta ou contate o '
                                                        'administrador'})
                else:
                    return render(request, 'user_app/register.html', {'error_message': 'Usuário inválido, crie outra '
                                                                                       'conta ou contate o administrador'})
            else:
                return render(request, 'user_app/login.html', {'error_message': 'Sua conta foi desconectada'})
        else:
            # 'Usuário ou senha inválidos'
            return render(request, 'user_app/login.html', {'error_message': 'Usuário e/ou senha inválidos'})
    return render(request, 'user_app/login.html')


def register(request):
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    funcs = Funcionalidades.objects.all()
    if request.user.is_authenticated():
        return render(request, 'user_app/index.html', {"funcs": funcs})
    elif request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['username']
            cpf = form.cleaned_data['cpf']
            email = form.cleaned_data['email']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            # check validity of cpf
            char_of_cpf = list(cpf)
            last = char_of_cpf.pop()
            penultimate = char_of_cpf.pop()
            weight = 10
            sum_ = 0
            cpf_is_valid = False

            # check penultimate digit
            for num in char_of_cpf:
                sum_ += int(num) * weight
                weight = weight - 1
            rest = 11 - (sum_ % 11)
            if rest > 9 and int(penultimate) == 0:
                cpf_is_valid = True
            elif rest == int(penultimate):
                cpf_is_valid = True

            # check last digit
            if cpf_is_valid:
                cpf_is_valid = False
                char_of_cpf.append(penultimate)
                sum_ = 0
                weight = 11
                for num in char_of_cpf:
                    sum_ += int(num) * weight
                    weight = weight - 1
                rest = 11 - (sum_ % 11)
                if rest > 9 and int(last) == 0:
                    cpf_is_valid = True
                elif rest == int(last):
                    cpf_is_valid = True

            if not cpf_is_valid:
                return render(request, 'user_app/register.html',
                              {"form": form, "error_message": "O CPF digitado não é válido"})

            if password1 != password2:
                return render(request, 'user_app/register.html',
                              {"form": form, "error_message": "As senhas devem ser iguais"})
            else:
                user = User.objects.create_user(username=cpf, email=email, password=password1, first_name=name)
                user.save()
                new_user = Custom_user(django_user=user)
                new_user.is_user = True
                new_user.save()
                actual_user = authenticate(username=cpf, password=password1)
                if actual_user is not None:
                    if user.is_active:
                        login(request, actual_user)
                        return render(request, 'user_app/index.html', {"funcs": funcs, "name": user.first_name})
                else:
                    return render(request, 'user_app/register.html', context)
        else:
            return render(request, 'user_app/register.html', context)
    else:
        return render(request, 'user_app/register.html', context)


def logout_user(request):
    logout(request)
    return render(request, 'user_app/login.html')


def code(request):
    return render(request, 'core_app/base_visitor.html')


def appointments(request):
    return render(request, 'core_app/base_visitor.html')


def health(request):
    return render(request, 'core_app/base_visitor.html')


def error(request):
    return render(request, 'core_app/base_visitor.html')


def graphics(request):
    return render(request, 'core_app/base_visitor.html')


def recipes(request):
    if not request.user.is_authenticated():
        return render(request, 'user_app/login.html')
    else:
        all_user_recipes = Recipe.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            shearched_names_and_places = all_user_recipes.filter(
                Q(doctor__icontains=query) | Q(place__icontains=query)
            ).distinct()
            context = {
                'query_result': shearched_names_and_places,
                'recipes': None,
                'all': False
            }
            return render(request, 'user_app/recipes.html', context)
        else:
            latest_10_recipes = all_user_recipes.order_by('-pub_date')[:10]
            context = {
                'recipes': latest_10_recipes,
                'query_result': None,
                'all': False
            }
            return render(request, 'user_app/recipes.html', context)


def show_all_recipes(request):
    if not request.user.is_authenticated():
        return render(request, 'user_app/login.html')
    else:
        all_user_recipes = Recipe.objects.filter(user=request.user)
        context = {
            'recipes': all_user_recipes,
            'query_result': None,
            'all': True
        }
        return render(request, 'user_app/recipes.html', context)


def notifications(request):
    return render(request, 'core_app/base_visitor.html')


def consultation(request):
    return render(request, 'core_app/base_visitor.html')