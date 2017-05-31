from django.conf.urls import url
from . import views

app_name = 'user_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^code/$', views.code, name='code'),
    url(r'^appointments/$', views.appointments, name='appointments'),
    url(r'^health/$', views.health, name='health'),
    url(r'^graphics/$', views.graphics, name='graphics'),
    url(r'^recipes/$', views.recipes, name='recipes'),
    url(r'^notifications/$', views.notifications, name='notifications'),
    url(r'^consultation/$', views.consultation, name='consultation'),
    url(r'^show_all_recipes/$', views.show_all_recipes, name='show_all_recipes'),

    #url(r'^recipes/$', CreateRecipe.as_view(), name='recipes'),
    #url(r'^recipes/$', UpdateUser.as_view(), name='recipes'),

]
