from django.contrib import admin
from .models import Usuario, Noticia, Denuncia
# Register your models here.
admin.site.register(Usuario)
admin.site.register(Noticia)
admin.site.register(Denuncia)