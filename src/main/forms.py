from django import forms

from .models import Noticia
from .models import Categoria
from .models import Usuario
from django.contrib.auth.forms import UserChangeForm
from .models import Denuncia
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


class NoticiaForm (forms.Form):
    titulo = forms.Textarea(attrs={'rows': 20, 'cols': 15})
    descripcion = forms.Textarea(attrs={'rows': 20, 'cols': 15})
    fuente = forms.CharField(max_length=100)
    pais = forms.CharField(max_length=20)

    def save(self, imagen, user, titulo, descripcion, categorias):
        data = self.cleaned_data
        noticia = Noticia(titulo=titulo, descripcion=descripcion,
                          fuente=data['fuente'], pais=data['pais'], puntaje=user.calc_puntaje(), imagen=imagen, creador=user)
        cats = []
        for cat in categorias.split(','):
            if not Categoria.objects.filter(nombre=cat).exists():
                new = Categoria(nombre=cat)
                new.save()
                cats.append(new)
            else:
                cats.append(Categoria.objects.get(nombre=cat))
        noticia.save()
        for cat in cats:
            noticia.categorias.add(cat)


class UsuarioForm (forms.Form):
    fecha_nacimiento = forms.DateField()
    nacionalidad = forms.CharField(max_length=20)
    puntaje = forms.IntegerField()
    genero = forms.CharField(max_length=10)
   # descripcion = forms.CharField(max_length=140)
    def save(self):
       data = self.cleaned_data
       usuario = Usuario(descripcion=data['descripcion'],  puntaje=0,
                         fecha_nacimiento=data[' fecha_nacimiento'], genero=data['genero'])
       usuario.save()



class DenunciaForm (forms.Form):
    descripcion = forms.CharField(max_length=500)
    email = forms.CharField(max_length=30)
    tipo = forms.CharField(max_length=30)
    def save(self, noticia):
        data = self.cleaned_data
        denuncia = Denuncia(descripcion=data['descripcion'], email=data['email'],
                          tipo=data['tipo'], noticia=noticia)
        denuncia.save()


class PerfilEditadoForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.CharField(max_length=100)

    def save(self, user, descripcion):
        data = self.cleaned_data
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.descripcion = descripcion
        user.save()


class PasswordForm(forms.Form):
    old_password = forms.CharField(max_length=100)
    new_password = forms.CharField(max_length=100)
    repeat_new_password = forms.CharField(max_length=100)

    def save(self, user):
        data = self.cleaned_data
        u = authenticate(username=user.username, password=data['old_password'])
        if u is not None and data['new_password'] == data['repeat_new_password']:
            user.set_password(data['new_password'])
            user.save()
            return True
        return False



