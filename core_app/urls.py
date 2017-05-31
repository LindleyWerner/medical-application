from django.conf.urls import url
from . import views

app_name = 'core_app'

urlpatterns = [
    url(r'^$', views.login_user, name='login'),
    url(r'^about/$', views.about, name='about'),
    url(r'^error/$', views.error, name='error'),
    url(r'^logout/$', views.logout_user, name='logout'),
    url(r'^pre_register/$', views.pre_register, name='pre_register'),
]