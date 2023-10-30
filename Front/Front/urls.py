from django.contrib import admin
from django.urls import path
from Front.view import inicio, Cargar, peticiones, prueba
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', inicio),
    path('cargarArchivo/', Cargar),
    path('peticiones/', peticiones),
    path('pruebas/', prueba)
]
urlpatterns += staticfiles_urlpatterns()