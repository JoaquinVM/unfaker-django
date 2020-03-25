from django.contrib import admin
from .models import Usuario, Noticia, Denuncia
from django.contrib.auth.admin import UserAdmin
# Register your models here.
admin.site.register(Usuario, UserAdmin)
admin.site.register(Noticia)
admin.site.register(Denuncia)
