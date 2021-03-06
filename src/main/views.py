import json
import urllib
from django.shortcuts import render, redirect
from .forms import NoticiaForm, DenunciaForm, UsuarioForm, PerfilEditadoForm, PasswordForm
from django.contrib.auth.models import auth, User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import Noticia
from django.http import HttpResponseNotFound

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
            if User.objects.filter(username=username).exists():
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

from django.db.models import Q
def explore_view(request, texto=None):
    noticias = Noticia.objects.all()
    context = {'word': "", 'categoria':""}
    if request.method == "POST":
        if "word" in request.POST:
            noticias = Noticia.objects.filter(titulo__icontains=request.POST['input'])
            context['word'] = request.POST['input']
        elif "categoria" in request.POST:
            q = Q()
            for tag in request.POST['input'].split(","):
                q |= Q(categorias__nombre__iexact=tag)
            noticias = Noticia.objects.filter(q)
            context['categoria'] = request.POST['input']
    elif texto:
        q = Q()
        for tag in [texto]:
            q |= Q(categorias__nombre__iexact=tag)
            noticias = Noticia.objects.filter(q)
            context['categoria'] = texto

    context['noticias'] = noticias

    return render(request, "explore.html", context)

def fresh_view(request):
    noticias = Noticia.objects.all()
    return render(request, "feed.html", {'noticias': noticias})

def following_view(request):
    noticias = Noticia.objects.filter(creador__in=request.user.siguiendo.all())
    return render(request, "feed.html", {'noticias': noticias})


def feed_view(request):
    noticias = Noticia.objects.filter(puntaje__gte=4)
    return render(request, "feed.html", {'noticias': noticias})


def new_view(request, id):
    form = DenunciaForm(request.POST or None)
    noticia = Noticia.objects.get(id=id)

    if request.method == "POST":
        if 'voto' in request.POST:
            voto = request.POST['debt-amount']
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
                noticia.actualizarPuntaje(request.user, voto, request.user.calc_puntaje())
            else:
                messages.error(request, '¿Eres un robot? ¡Captcha inválido!')

        if 'denuncia' in request.POST:
            if form.is_valid():
                form.save(noticia)
        if 'seguir' in request.POST:
            if noticia.creador not in request.user.siguiendo.all():
                request.user.siguiendo.add(noticia.creador)
            else:
                request.user.siguiendo.remove(noticia.creador)

    context = {
        'noticia': noticia,
        'no_voto': request.user not in noticia.usuarios.all()
    }
    if noticia.creador in request.user.siguiendo.all():
        context['follow'] = "Unfollow"
    else:
        context['follow'] = "Follow"

    return render(request, "noticia.html", context)


def profile_view(request):
    form = UsuarioForm(request.POST or None)
    noticias = Noticia.objects.filter(creador=request.user)
    siguiendo = request.user.siguiendo.all()
    if form.is_valid():
        form.save()
    context = {
        'form': form,
        'noticias': noticias,
        'siguiendo': siguiendo,
        'user': request.user
    }
    return render(request, "profile.html", context)


def profileedit_view(request):
    form = PerfilEditadoForm(request.POST or None)
    if request.method == 'POST' and 'edit' in request.POST:
        form = PerfilEditadoForm(request.POST)
        if form.is_valid():
            if 'imagen' in request.FILES:
                myfile = request.FILES['imagen']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile) # saves the file to `media` folder
                uploaded_file_url = fs.url(filename) # gets the url
                request.user.imagen = filename
                request.user.save()

            form.save(request.user, request.POST['descripcion'])
            return render(request, 'profileedit.html')
        else:
            args= {'form': form, 'messages': form.errors}
            messages.error(request, form.errors)
            return render(request, 'profileedit.html', args)
    if request.method == 'POST' and 'password' in request.POST:
        form = PasswordForm(request.POST)
        if form.is_valid():
            if form.save(request.user):
                return render(request, 'profileedit.html')
            else:
                args= {'form': form}
                messages.info(request, "Invalid Data")
                return render(request, 'profileedit.html', args)
        else:
            args= {'form': form}
            messages.info(request, "Invalid Data")
            return render(request, 'profileedit.html', args)

    context = {
        'form1': form,
        'user': request.user
    }
    return render(request, "profileedit.html", context)

def publish_view(request):
    form = NoticiaForm(request.POST or None)

    context = {'user': request.user}

    if request.method == 'POST':
        if 'imagen' in request.FILES and form.is_valid():
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
                myfile = request.FILES['imagen']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile) # saves the file to `media` folder
                uploaded_file_url = fs.url(filename) # gets the url
                form.save(filename, request.user, request.POST['titulo'], request.POST['descripcion'], request.POST['categorias'])
                context['uploaded_file_url'] = uploaded_file_url
                messages.info(request, 'tu noticia ha sido publicada con éxito')
                return render(request, 'publish.html', context)
            else:
                messages.error(request, '¿Eres un robot? ¡Captcha inválido!')

        else:
            messages.info(request, 'Datos invalidos')

    return render(request, 'publish.html', context)

def logout_view(request):
    auth.logout(request)
    return redirect('/')

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

def change_password_view(request):
    form = PasswordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save(request.user, request.POST['descripcion'])
            return render(request, 'profileedit.html')
        else:
            args= {'form': form, 'messages': form.errors}
            messages.error(request, form.errors)
            return render(request, 'profileedit.html', args)
    context = {
        'form2': form
    }
    return render(request, 'profileedit.html', context)

from django.shortcuts import render
from django.template import loader
def error404(request, template_name='main/error404.html'):
    t = loader.get_template(template_name)
    context = {
        'your_var' : True,
        'request' : request,
    }
    return HttpResponseNotFound(t.render(context))

def error500(request):
    return render(request,'error500.html', status=500)