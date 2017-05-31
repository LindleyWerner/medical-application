from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .models import *
from .forms import UserForm
from django.contrib.auth.models import User
from django.db.models import Q
# from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.
def index(request):
    valid_user = __is_valid_user(request)
    if valid_user is True:
        context = {'user_type': 'User', 'funcs': Funcionalidade.objects.all(), 'name': request.user.first_name}
        return render(request, 'user_app/index.html', context)
    return valid_user


def user_login(request, user):
    context = {'user_type': None}
    if user is not None:
        login(request, user)
        context['funcs'] = Funcionalidade.objects.all()
        context['name'] = user.first_name
        context['user_type'] = 'User'
        return render(request, 'user_app/index.html', context)
    else:
        context['error_message'] = 'Erro desconhecido tente se conectar novamente, se persistir '\
                                    'contate o administrador'
        return render(request, 'core_app/login.html', context)


def register(request):
    form = UserForm(request.POST or None)
    context = {
        "form": form,
        "user_type": None
    }
    if __is_valid_user(request) is True:
        context['funcs'] = Funcionalidade.objects.all()
        context.pop('form')
        context['user_type'] = 'User'
        context['name'] = request.user.first_name
        return render(request, 'user_app/index.html', context)
    elif request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['username']
            email = form.cleaned_data['email']
            cpf = form.cleaned_data['cpf']
            birth_date = form.cleaned_data['birth_date']
            gender = form.cleaned_data['gender']
            address = form.cleaned_data['address']
            phones = form.cleaned_data['phones']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            if not __check_cpf(cpf):
                context['error_message'] = "O CPF digitado não é válido"
                return render(request, 'core_app/register.html', context)

            if password1 != password2:
                context['error_message'] = "As senhas devem ser iguais"
                return render(request, 'core_app/register.html', context)
            else:
                name_list = name.split()
                user = User.objects.create_user(username=email, email=email, password=password1,
                                                first_name=name_list[0], last_name=name_list[-1])
                user.save()
                new_user = Simple_user(django_user=user, full_name=name, birth_date=birth_date,
                                       gender=gender, address=address, phones=phones)
                new_user.save()
                actual_user = authenticate(username=email, password=password1)
                if actual_user is not None:
                    if user.is_active:
                        login(request, actual_user)
                        context['funcs'] = Funcionalidade.objects.all()
                        context['name'] = user.first_name
                        context['user_type'] = 'User'
                        context.pop('form')
                        return render(request, 'user_app/index.html', context)
    return render(request, 'core_app/register.html', context)


def code(request):
    valid_user = __is_valid_user(request)
    if valid_user is True:
        context = {'user_type': 'User', 'func': 'Código'}
        return render(request, 'user_app/test.html', context)
    return valid_user


def appointments(request):
    valid_user = __is_valid_user(request)
    if valid_user is True:
        context = {'user_type': 'User', 'func': 'Marcações'}
        return render(request, 'user_app/test.html', context)
    return valid_user


def health(request):
    valid_user = __is_valid_user(request)
    if valid_user is True:
        context = {'user_type': 'User', 'func': 'Saúde'}
        return render(request, 'user_app/test.html', context)
    return valid_user


def graphics(request):
    valid_user = __is_valid_user(request)
    if valid_user is True:
        context = {'user_type': 'User', 'func': 'Gráficos'}
        return render(request, 'user_app/test.html', context)
    return valid_user


def recipes(request):
    valid_user = __is_valid_user(request)
    if valid_user is True:
        context = {'user_type': 'User'}
        all_user_recipes = Recipe.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            shearched_names_and_places = all_user_recipes.filter(
                Q(doctor__icontains=query) | Q(place__icontains=query)
            ).distinct()
            context['query_result'] = shearched_names_and_places
            context['recipes'] = None
            return render(request, 'user_app/recipes.html', context)
        else:
            latest_10_recipes = all_user_recipes.order_by('-pub_date')[:10]
            context['query_result'] = None
            context['recipes'] = latest_10_recipes
            return render(request, 'user_app/recipes.html', context)
    return valid_user


def show_all_recipes(request):
    valid_user = __is_valid_user(request)
    if valid_user is True:
        all_user_recipes = Recipe.objects.filter(user=request.user)
        context = {'user_type': 'User', 'query_result': None, 'recipes': all_user_recipes}
        return render(request, 'user_app/recipes.html', context)
    return valid_user


def notifications(request):
    valid_user = __is_valid_user(request)
    if valid_user is True:
        context = {'user_type': 'User', 'func': 'Notificações'}
        return render(request, 'user_app/test.html', context)
    return valid_user


def consultation(request):
    valid_user = __is_valid_user(request)
    if valid_user is True:
        context = {'user_type': 'User', 'func': 'Consultas'}
        return render(request, 'user_app/test.html', context)
    return valid_user


'''class CreateRecipe(CreateView):
    model = Recipe
    template_name = "user_app/create.html"
    fields = ['user','doctor','description','pub_date','place']

    def get_context_data(self, **kwargs):
        context = super(CreateRecipe, self).get_context_data(**kwargs)
        context["objects"] = self.model.objects.all()
        return context'''

'''
#self.kwargs['id'], parece que este kwargs vem da url e.g. portfolios/update/(?P<id>\d+)/
class UpdateUser(UpdateView):
    model = Custom_user
    template_name = "user_app/create.html"
    form_class = UserForm

    def get_object(self, queryset=None):
        obj = Custom_user.objects.get(id=self.kwargs['id'])
        return obj'''


def __check_cpf(cpf):
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
    return cpf_is_valid


def __is_valid_user(request):
    context = {'user_type': None}
    if request.user.is_authenticated():
        if request.user.groups.filter(name='User').exists():
            return True
    context['error_message'] = 'Você precisa estar autenticado como usuário para acessar esta funcionalidade'
    return render(request, 'core_app/login.html', context)
