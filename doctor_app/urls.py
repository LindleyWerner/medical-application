from django.conf.urls import url
from . import views

app_name = 'doctor_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^code/$', views.code, name='code'),
    url(r'^patient/$', views.patient, name='patient'),
    url(r'^consultation/$', views.consultation, name='consultation'),
    url(r'^documents/$', views.documents, name='documents'),
]