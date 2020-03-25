import json
import urllib
from django.shortcuts import render, redirect
from .forms import NoticiaForm
from .forms import DenunciaForm
from .forms import UsuarioForm
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings

User = get_user_model()
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
                ###
                recaptcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                values = {
                    'secret': settings.RECAPTCHA_SECRET_KEY,
                    'response': recaptcha_response
                }
                data = urllib.parse.urlencode(values).encode()
                req = urllib.request.Request(url, data=data)
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())
                if result['success']:
                    user = User.objects.create_user(username=username, password=contrasena1, email=email,
                                                    nacionalidad=nacionalidad, fecha_nacimiento=fecha_nacimiento,
                                                    first_name=nombre, last_name=apellido, puntaje=0)
                    user.save()
                    messages.success(request, 'Usuario creado')
                    return redirect('login')
                else:
                    messages.error(request, '¿Eres un robot? ¡Captcha inválido!')
                    return redirect('signin')



                ###
                #user=User.objects.create_user(username=username, password=contrasena1, email=email, nacionalidad= nacionalidad,
                 #                     fecha_nacimiento=fecha_nacimiento, first_name=nombre, last_name=apellido, puntaje=0)
                #user.save();
                #messages.info(request,'Usuario creado')
                #return redirect('login')

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
            auth.login(request, user)
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

    if request.method == 'POST' and request.FILES['imagen'] and form.is_valid():
        myfile = request.FILES['imagen']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile) # saves the file to `media` folder
        uploaded_file_url = fs.url(filename) # gets the url
        form.save(filename)
        return render(request, 'publish.html', {
            'uploaded_file_url': uploaded_file_url})

def logout_view(request):
    auth.logout(request)
    return redirect('/')

    return render(request, 'publish.html')
    # form = NoticiaForm(request.POST or None)
    # if form.is_valid() and request.POST.get('imagen', False):
    #     imagen = request.POST.get('imagen', False)
    #     fs = FileSystemStorage()
    #     filename = fs.save(imagen.name, imagen)
    #     form.save(imagen=filename)
    # context = {
    #     'form': form
    # }
    # return render(request, "publish.html", context)
