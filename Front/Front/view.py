from django.http import HttpResponse
from django.template import loader
from requests import post, get

def getInfoEstudiante(request):
    return HttpResponse("Frontend: Estudiante de IPC2")

def reporte(reques):

    url = "http://127.0.0.1:3050/"
    respuesta = get(url)
    print(respuesta.json())

    existe = False
    namereporte =  "Sentimiento de mensaje"
    descripcion = "Reporte de sentimientos de mensaje"
    conteo = [10,20,50]

    objtmp = loader.get_template("reporte.html")
    html = objtmp.render({"existe":existe,"respue":respuesta.json(),"idNombre_reporte":namereporte, "descripcion":descripcion, "valores":conteo})
    return HttpResponse(html)