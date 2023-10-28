from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.template import loader
from requests import post, get

def inicio(request):
    objtmp = loader.get_template("index.html")
    html = objtmp.render()
    return HttpResponse(html)

def Cargar(request):
    if 'file' in request.FILES:
        archivo = request.FILES['file']
        url = "http://127.0.0.1:3050/grabarMensajes"
        mensaje = post(url, files= request.FILES)
        if mensaje.json().get("message") == "Carga exitosa":
            texto = mensaje.json().get("message")
            return render(request,'Pagina1.html', {"mensaje":texto})

    return render(request,'Pagina1.html')

def reporte(reques):

    #url = "http://127.0.0.1:3050/"
    #respuesta = get(url)
    #print(respuesta.json())

    existe = False
    namereporte =  "Sentimiento de mensaje"
    descripcion = "Reporte de sentimientos de mensaje"
    conteo = [10,20,50]

    objtmp = loader.get_template("index.html")
    #"respue":respuesta.json()
    html = objtmp.render({"existe":existe,"idNombre_reporte":namereporte, "descripcion":descripcion, "valores":conteo})
    return HttpResponse(html)