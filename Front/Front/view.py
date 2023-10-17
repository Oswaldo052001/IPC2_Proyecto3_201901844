from django.http import HttpResponse
from django.template import loader
from requests import post, get

def inicio(request):
    objtmp = loader.get_template("index.html")
    html = objtmp.render()
    return HttpResponse(html)


def enlace1(request):
    objtmp = loader.get_template("Pagina1.html")
    html = objtmp.render()
    return HttpResponse(html)


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