from django import forms

from django.db.models import Noticia

class NoticiaForm (forms.ModelForm):
    class Meta:
        fields:['titulo', 'descripcion', 'fuente', 'creador', 'fecha', 'pais', 'imagen']
        labels= {'titulo': 'Titulo', 'descripcion': 'Descripcion', 'fuente': 'Fuente', 'creador': 'Creador',
                 'fecha': 'Fecha', 'pais': 'Pais', 'imagen': 'Imagen'}
        widgets= {}