from django.http import HttpResponse
from django.template import Template, Context, loader

def saludo(request):
    return HttpResponse("Hola Django equipo coder")


def segunda_vista(request):
    return HttpResponse("<br><br> <h1>Hola mundo!<h1>")

def miNombreEs(self, nombre):
    data = f"Mi nombre es: <h1>{nombre}<h1>"
    return HttpResponse(data)

def probandoTemplate(self):
    nombre = "Joaquin"
    apellido = "Sanchez"

    namelist = ["Gabriel","Jimena","Ignacio","Patricia","Natalia"]

    diccionario = {
        "nombre" : nombre,
        "apellido" : apellido,
        "namelist" : namelist
    }

    #miHtml = open("/Users/joacosanchez/Documents/Visual Studio/Python 2/CoderHouse 2023/PythonProyecto1/Proyecto1/Proyecto1/plantillas/template1.html")
    #loader.get_template("template1.html")
    plantilla = loader.get_template("template1.html")
    #miHtml.close()
    #miContext = Context(diccionario)
    documento = plantilla.render(diccionario)
    return HttpResponse(documento)