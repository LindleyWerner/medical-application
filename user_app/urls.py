from django.conf.urls import url
from . import views

app_name = 'user_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^code/$', views.code, name='code'),
    url(r'^appointments/$', views.appointments, name='appointments'),
    url(r'^health/$', views.health, name='health'),
    url(r'^error/$', views.error, name='error'),
    url(r'^graphics/$', views.graphics, name='graphics'),
    url(r'^recipes/$', views.recipes, name='recipes'),
    url(r'^notifications/$', views.notifications, name='notifications'),
    url(r'^consultation/$', views.consultation, name='consultation'),
    url(r'^show_all_recipes/$', views.show_all_recipes, name='show_all_recipes'),
]
