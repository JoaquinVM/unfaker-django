from django import forms

from .models import Noticia
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Denuncia



class NoticiaForm (forms.Form):
    titulo = forms.Textarea(attrs={'rows': 20, 'cols': 15})
    descripcion = forms.Textarea(attrs={'rows': 20, 'cols': 15})
    fuente = forms.CharField(max_length=100)
    pais = forms.CharField(max_length=20)

    def save(self, imagen, user, titulo, descripcion):
        data = self.cleaned_data
        noticia = Noticia(titulo=titulo, descripcion=descripcion,
                          fuente=data['fuente'], pais=data['pais'], puntaje=0, imagen=imagen, creador=user)
        noticia.save()


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
        fields = [ 'first_name', 'last_name', 'email']

