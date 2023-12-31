from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from AppCoder.models import Estudiante, Avatar
from AppCoder.forms import formSetEstudiante, UserEditForm, ChangePasswordForm, AvatarForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login,logout,authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

@login_required
def inicio(request):
    avatar = getavatar(request)
    return render(request, "AppCoder/inicio.html", {"avatar": avatar})

def cursos(request):
    return render(request, "AppCoder/cursos.html")

def profesores(request):
    return render(request, "AppCoder/profesores.html")

def estudiantes(request):
    Estudiantes = Estudiante.objects.all()
    return render(request, "AppCoder/estudiantes.html", {"Estudiantes": Estudiantes})

def entregables(request):
    return render(request, "AppCoder/entregables.html")

@login_required
def setEstudiantes(request):
    Estudiantes = Estudiante.objects.all()

    #formulatio con html
    if request.method == 'POST':
        estudiante = Estudiante(nombre=request.POST["nombre"],apellido=request.POST["apellido"],email=request.POST["email"]) #modelo
        estudiante.save()
        miFormulario = formSetEstudiante() #aqui limpiamos el formulario despues de enviarlo
        return render(request, "AppCoder/setEstudiantes.html", {"miFormulario":miFormulario, "Estudiantes": Estudiantes}) #redirijo a la misma web donde cargo el formulario

    ##formulario con API de django
    #if request.method == 'POST':
    #    miFormulario = formSetEstudiante(request.POST)
    #    print(miFormulario)
    #    if miFormulario.is_valid:
    #        data = miFormulario.cleaned_data
    #        estudiante = Estudiante(nombre=data["nombre"],apellido=data["apellido"],email=data["email"]) #modelo
    #        estudiante.save()
    #        #return render(request, "AppCoder/inicio.html")
    #        miFormulario = formSetEstudiante() #aqui limpiamos el formulario despues de enviarlo
    #        return render(request, "AppCoder/setEstudiantes.html", {"miFormulario":miFormulario, "Estudiantes": Estudiantes}) #redirijo a la misma web donde cargo el formulario

    else:
        miFormulario = formSetEstudiante()
    
    return render(request, "AppCoder/setEstudiantes.html", {"miFormulario":miFormulario, "Estudiantes": Estudiantes})

    #formulatio con html
    """if request.method == 'POST':
        estudiante = Estudiante(nombre=request.POST["nombre"],apellido=request.POST["apellido"],email=request.POST["email"]) #modelo
        estudiante.save()
        return render(request, "AppCoder/inicio.html")
    return render(request, "AppCoder/setEstudiantes.html")"""

def getEstudiantes(request):
    return render(request, "AppCoder/getEstudiantes.html")

def buscarEstudiante(request):
    if request.GET["nombre"]:
        nombre = request.GET["nombre"]
        estudiantes = Estudiante.objects.filter(nombre = nombre)
        return render(request, "AppCoder/getEstudiantes.html", {"estudiantes":estudiantes})
    else:
        respuesta = "No se enviaron datos"
    return HttpResponse(respuesta)

#def leerEstudiantes(request):
#    Estudiantes = Estudiante.objects.all()
#    return render(request, "AppCoder/estudiantes.html", {"Estudiantes": Estudiantes})

def eliminarEstudiante(request, nombre_estudiante):
    estudiante = Estudiante.objects.get(nombre = nombre_estudiante)
    estudiante.delete()
    miFormulario = formSetEstudiante()
    Estudiantes = Estudiante.objects.all
    return render(request, "AppCoder/setEstudiantes.html", {"miFormulario":miFormulario, "Estudiantes": Estudiantes})

def editarEstudiante(request, nombre_estudiante):
    estudiante = Estudiante.objects.get(nombre = nombre_estudiante)

    if request.method == 'POST':
        miFormulario = formSetEstudiante(request.POST)
        if miFormulario.is_valid:
            print(miFormulario)
            data = miFormulario.cleaned_data

            estudiante.nombre = data['nombre']
            estudiante.apellido = data['apellido']
            estudiante.email = data['email']
            estudiante.save()
            miFormulario = formSetEstudiante()
            Estudiantes = Estudiante.objects.all()
            return render(request, "AppCoder/setEstudiantes.html", {"miFormulario":miFormulario, "Estudiantes": Estudiantes})

    else:
        miFormulario = formSetEstudiante(initial={'nombre':estudiante.nombre, 'apellido': estudiante.apellido, 'email': estudiante.email})
    return render(request, "AppCoder/editarEstudiante.html", {"miFormulario":miFormulario})

def loginWeb(request):
    if request.method == "POST":
        user = authenticate(username = request.POST['user'], password = request.POST['password'])
        if user is not None:
            login(request, user)
            return render(request, "AppCoder/inicio.html")
        else:
            return render(request, 'AppCoder/login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'AppCoder/login.html')

def registro(request):
    if request.method == "POST":
        userCreate = UserCreationForm(request.POST)
        if userCreate is not None:
            userCreate.save()
            return render(request, 'AppCoder/login.html')
    else:
        return render(request, 'AppCoder/registro.html')
    
@login_required
def perfilview(request):
    return render(request, 'AppCoder/Perfil/Perfil.html')

@login_required
def editarPerfil(request):
    usuario = request.user
    user_basic_info = User.objects.get(id = usuario.id)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance = usuario)
        if form.is_valid():
            user_basic_info.username = form.cleaned_data.get('username')
            user_basic_info.email = form.cleaned_data.get('email')
            user_basic_info.first_name = form.cleaned_data.get('first_name')
            user_basic_info.last_name = form.cleaned_data.get('last_name')
            user_basic_info.save()
            return render(request, 'AppCoder/Perfil/Perfil.html')
    else:
            form = UserEditForm(initial = {'username':usuario.username, 'email':usuario.email, 'first_name':usuario.first_name, 'last_name':usuario.last_name})
            return render(request, 'AppCoder/Perfil/editarPerfil.html', {"form": form})
        
@login_required
def changePassword(request):
    usuario = request.user
    if request.method == "POST":
        form = ChangePasswordForm(data = request.POST, user = usuario)
        if form.is_valid():
            if request.POST['new_password1'] == request.POST['new_password2']:
                user = form.save()
                update_session_auth_hash(request, user)
            return HttpResponse("Las contraseñas no coinciden")
        return render(request, "AppCoder/inicio.html")
    else:
        form = ChangePasswordForm(user = usuario)
        return render(request, "AppCoder/Perfil/changePassword.html", {"form":form})

def editAvatar(request):
    if request.method == "POST":
        form = AvatarForm(request.POST, request.FILES)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            user = User.objects.get(username = request.user)
            avatar = Avatar(user = user, image = form.cleaned_data['avatar'], id = request.user.id)
            avatar.save()
            avatar = Avatar.objects.filter(user = request.user.id)
            try:
                avatar = avatar[0].image.url
            except:
                avatar = None
            return render(request, 'AppCoder/inicio.html', {'avatar':avatar})
    else:
        try:
            avatar = Avatar.objects.filter(user = request.user.id)
            form = AvatarForm()
        except:
            form = AvatarForm()
    return render(request, 'AgregarAvatar.html', {'form': form})

def getavatar(request):
    avatar = Avatar.objects.filter(user = request.user.id)
    try:
        avatar = avatar[0].image.url
    except:
        return avatar