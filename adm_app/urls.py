from django.conf.urls import url
from . import views

app_name = 'adm_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
]