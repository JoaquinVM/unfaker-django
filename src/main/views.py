from django.shortcuts import render, redirect
from .forms import NoticiaForm
from .forms import DenunciaForm
#from .forms import UsuarioForm
from django.contrib import messages
from django.contrib.auth.models import User, auth

# Create your views here.
def signin_view(request):
    if request.method== 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        username = request.POST['username']
        email = request.POST['email']
        fecha_nacimiento = request.POST['fecha_nacimiento']
        nacionalidad = request.POST['nacionalidad']
        contrasena1 = request.POST['contrasena1']
        contrasena2 = request.POST['contrasena2']
        if contrasena1==contrasena2:
            if User .objects.filter(username=username).exists():
                messages.info(request,'Usuario ya usado')
                return redirect('signin')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email ya usado')
                return redirect('signin')
            else:
                user=User.objects.create_user(username=username,contrasena1=contrasena1, email=email, nacionalidad=nacionalidad,
                                      fecha_nacimiento=fecha_nacimiento,nombre=nombre,apellido=apellido)
                user.save();
                messages.info(request,'Usuario creado')
                return redirect('login')
        else:
            messages.info(request,'Contraseñas diferentes')
            return redirect('signin')
        return redirect('/')
    else:
        return render(request, "signin.html")

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request, 'Credencial invalida')
            return redirect('login')
    else:
        return render(request, "login.html")

def feed_view(request):
    return render(request, "feed.html", {})


def new_view(request):
    form = DenunciaForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "noticia.html", context)


def profile_view(request):
    form = UsuarioForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "profile.html", context)


def publish_view(request):
    form = NoticiaForm(request.POST or None)
    if form.is_valid():
        form.save()
    context = {
        'form': form
    }
    return render(request, "publish.html", context)
