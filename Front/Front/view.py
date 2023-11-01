from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.template import loader
from requests import post, get
import xml.etree.ElementTree as ET
import json


def inicio(request):
    objtmp = loader.get_template("index.html")
    html = objtmp.render()
    return HttpResponse(html)

def Cargar(request):
    if 'file' in request.FILES:
        try:
            archivo = request.FILES['file']
            url = "http://127.0.0.1:3050/grabarMensajes"
            mensaje = post(url, files= request.FILES)
            if mensaje.json().get("message") == "Carga exitosa":
                texto = mensaje.json().get("message")
                return render(request, 'CargarArchivo.html', {"mensaje":texto})
        except:
            mensaje = "VERIFIQUE CONEXIÓN CON EL SERVIDOR"
            return render(request, 'CargarArchivo.html', {"mensaje":mensaje})
    return render(request, 'CargarArchivo.html')

def peticiones(request):

    if request.method == "POST":
        lista = request.POST.getlist('select')
        opcion = ""
        for escogido in lista:
            opcion = escogido

        try:
            if opcion == "Hashtag":
                url = "http://127.0.0.1:3050/devolverHashtags"
                mensaje = post(url, data=request.POST)
                ruta = 'DateBase/PeticionesHashtags.xml'
                archivo = ET.parse(ruta).getroot()
                valores = []
                valor = dict()
                hashtagas = archivo.find('hashtags')
                for fecha in hashtagas.findall('fecha'):
                    valor = {'fecha': fecha.get('fecha')}
                    for hastag in fecha.findall('hashtag'):
                        valor[hastag.text] = hastag.get('cantidad')
                    valores.append(valor)

                mensaje = ""
                if len(valores) == 0:
                    mensaje = "No se encontraron datos para esta petición"
                else:
                    mensaje = "Petición realizada con exito"

                return render(request, 'Peticiones.html', {"valores": valores, "mensaje": mensaje})

            if opcion == "Menciones":
                url = "http://127.0.0.1:3050/devolverMenciones"
                mensaje = post(url, data=request.POST)
                ruta = 'DateBase/PeticionesMenciones.xml'
                archivo = ET.parse(ruta).getroot()
                valores = []
                valor = dict()
                usuarios = archivo.find('usuarios')
                for fecha in usuarios.findall('fecha'):
                    valor = {'fecha': fecha.get('fecha')}
                    for hastag in fecha.findall('usuario'):
                        valor[hastag.text] = hastag.get('cantidad')
                    valores.append(valor)

                mensaje = ""
                if len(valores) == 0:
                    mensaje = "No se encontraron datos para esta petición"
                else:
                    mensaje = "Petición realizada con exito"
                return render(request, 'Peticiones.html', {"valores": valores, "mensaje":mensaje})

            if opcion == "Sentimientos":
                url = "http://127.0.0.1:3050/devolverSentimientos"
                mensaje = post(url, data=request.POST)
                ruta = 'DateBase/PeticionesSentimientos.xml'
                archivo = ET.parse(ruta).getroot()
                valores = []
                valor = dict()
                sentimientos = archivo.find('Sentimientos')
                for fecha in sentimientos.findall('fecha'):
                    valor = {'fecha': fecha.get('fecha')}
                    sentiposi = fecha.find('Mensajes_positivos')
                    sentinega = fecha.find('Mensajes_negativos')
                    sentineutro = fecha.find('Mensajes_nuetros')
                    valor["Sentimientos positivos"] = sentiposi.text
                    valor["Sentimientos negativos"] = sentinega.text
                    valor["Sentimientos neutros"] = sentineutro.text
                    valores.append(valor)
                mensaje = ""
                if len(valores) == 0:
                    mensaje = "No se encontraron datos para esta petición"
                else:
                    mensaje = "Petición realizada con exito"
                return render(request, 'Peticiones.html', {"valores": valores, "mensaje": mensaje})
        except:
            mensaje = "VERIFIQUE CONEXIÓN CON EL SERVIDOR"
            return render(request, 'Peticiones.html', {"mensaje": mensaje})
    return render(request, 'Peticiones.html')

def eliminar(request):
    try:
        url = "http://127.0.0.1:3050/limpiarDatos"
        mensaje = post(url)
        return render(request, 'eliminar.html', {'mensaje': mensaje.json().get("message")})
    except:
        mensaje = "VERIFIQUE CONEXIÓN CON EL SERVIDOR"
        return render(request, 'eliminar.html', {'mensaje': mensaje})
def ayuda(request):
    return render(request, 'ayuda.html')

def reporteConfiguraciones(request):
    return render(request, 'reporte.html')

def reporteDiccionario(request):
    return render(request, 'reporteDiccionario.html')
