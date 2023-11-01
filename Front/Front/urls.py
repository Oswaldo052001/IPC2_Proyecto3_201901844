from django.contrib import admin
from django.urls import path
from Front.view import inicio, Cargar, peticiones, eliminar, reporteConfiguraciones, reporteDiccionario, ayuda
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', inicio),
    path('cargarArchivo/', Cargar),
    path('peticiones/', peticiones),
    path('reporteConfi/', reporteConfiguraciones),
    path('reporteDicc/', reporteDiccionario),
    path('delete/', eliminar),
    path('ayuda/', ayuda)
]
urlpatterns += staticfiles_urlpatterns()