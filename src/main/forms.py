from django import forms

from .models import Noticia
from .models import Categoria
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Denuncia



class NoticiaForm (forms.Form):
    titulo = forms.Textarea(attrs={'rows': 20, 'cols': 15})
    descripcion = forms.Textarea(attrs={'rows': 20, 'cols': 15})
    fuente = forms.CharField(max_length=100)
    pais = forms.CharField(max_length=20)

    def save(self, imagen, user, titulo, descripcion, categorias):
        data = self.cleaned_data
        noticia = Noticia(titulo=titulo, descripcion=descripcion,
                          fuente=data['fuente'], pais=data['pais'], puntaje=0, imagen=imagen, creador=user)
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
    def save(self):
        data = self.cleaned_data
        denuncia = Denuncia(descripcion=data['descripcion'], email=data['email'],
                          tipo=data['tipo'])
        denuncia.save()

class PerfilEditadoForm(UserChangeForm):
    class Meta:
        model = User
        fields= ('email', 'username', 'first_name', 'last_name')
