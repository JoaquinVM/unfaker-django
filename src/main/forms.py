from django import forms

from .models import Noticia
#from .models import Usuario
from .models import Denuncia



class NoticiaForm (forms.Form):
    titulo = forms.CharField(max_length=100)
    descripcion = forms.CharField(max_length=500)
    fuente = forms.CharField(max_length=100)
    pais = forms.CharField(max_length=20)

    def save(self, imagen):
        data = self.cleaned_data
        noticia = Noticia(titulo=data['titulo'], descripcion=data['descripcion'],
                          fuente=data['fuente'], pais=data['pais'], puntaje=0, imagen=imagen)
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
