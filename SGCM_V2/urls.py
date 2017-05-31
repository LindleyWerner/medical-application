from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^core_app/', include('core_app.urls')),
    url(r'^user_app/', include('user_app.urls')),
    url(r'^doctor_app/', include('doctor_app.urls')),
    url(r'^adm_app/', include('adm_app.urls')),
    url(r'^', include('core_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)