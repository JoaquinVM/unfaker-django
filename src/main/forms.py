from django import forms

from .models import Noticia

class NoticiaForm (forms.Form):
    titulo = forms.CharField(max_length=100)
    descripcion = forms.CharField(max_length=500)
    fuente = forms.CharField(max_length=100)
    pais = forms.CharField(max_length=20)
    imagen= forms.ImageField()
    def save(self):
        data = self.cleaned_data
        noticia = Noticia(titulo=data['titulo'], descripcion=data['descripcion'],
                          fuente=data['fuente'], pais=data['pais'], puntaje=0, imagen=[''])
        noticia.save()

