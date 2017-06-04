from django.conf.urls import url
from . import views

app_name = 'adm_app'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^add-adm/$', views.add_adm, name='add_adm'),
    url(r'^remove-adm/(?P<adm_id>[0-9]+)/$', views.rm_adm, name='rm_adm'),
    url(r'^list-adm/$', views.list_adm, name='list_adm'),
    url(r'^add-doctor/$', views.add_doctor, name='add_doctor'),
    url(r'^remove-doctor/(?P<doctor_id>[0-9]+)/$', views.rm_doctor, name='rm_doctor'),
    url(r'^list-doctor/$', views.list_doctor, name='list_doctor'),
    url(r'^pending/$', views.list_pending_solicitations, name='list_pending_solicitations'),
    url(r'^remove-pending-adm/(?P<pending_adm_id>[0-9]+)/$', views.rm_pending_adm, name='rm_pending_adm'),
    url(r'^remove-pending-doctor/(?P<pending_doctor_id>[0-9]+)/$', views.rm_pending_doctor, name='rm_pending_doctor'),
]