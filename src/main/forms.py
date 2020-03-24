from django import forms

from .models import Noticia
#from .models import Usuario
from .models import Denuncia

class NoticiaForm (forms.Form):
    titulo = forms.CharField(max_length=100)
    descripcion = forms.CharField(max_length=500)
    fuente = forms.CharField(max_length=100)
    pais = forms.CharField(max_length=20)
    imagen= forms.FileField()
    def save(self):
        data = self.cleaned_data
        noticia = Noticia(titulo=data['titulo'], descripcion=data['descripcion'],
                          fuente=data['fuente'], pais=data['pais'], puntaje=0)
        noticia.save()


#class UsuarioForm (forms.Form):
 #   nombre = forms.CharField(max_length=50)
  #  apellido = forms.CharField(max_length=50)
   # username = forms.CharField(max_length=7)
    #contrasena1 = forms.CharField(max_length=20)
    #contrasena2 = forms.CharField(max_length=20)
    #email = forms.CharField(max_length=30)
    #fecha_nacimiento = forms.DateField()
    #  nacionalidad=models.CharField(choices=nacionalidades, default='Bolivia', max_length=20)
   # puntaje = forms.IntegerField()
   # genero = forms.CharField(max_length=10)
   # def save(self):
    #    data = self.cleaned_data
    #    usuario = Usuario(nombre=data['nombre'], apellido=data['apellido'],
    #                      username=data['username'], contrasena1=data['contrasena1'], puntaje=0,email=data['email'],
    #                      fecha_nacimiento=data[' fecha_nacimiento'], genero=data['genero'])
    #    usuario.save()


class DenunciaForm (forms.Form):
    descripcion = forms.CharField(max_length=500)
    email = forms.CharField(max_length=30)
    tipo = forms.CharField(max_length=30)
    def save(self):
        data = self.cleaned_data
        denuncia = Denuncia(descripcion=data['descripcion'], email=data['email'],
                          tipo=data['tipo'])
        denuncia.save()
