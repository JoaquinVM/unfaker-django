from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    id = models.AutoField(primary_key = True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=7, unique=True)
    password = models.CharField(default='', max_length=20)
    email = models.CharField(max_length=30, default='')
    fecha_nacimiento = models.DateField(null=True)
    nacionalidades=  (('Argentina', 'Argentina'), ('Bolivia', 'Bolivia'), ('Brasil', 'Brasil'),
              ('Chile', 'Chile'), ('Colombia', 'Colombia'), ('Ecuador', 'Ecuador'),
              ('Paraguay', 'Paraguay'), ('Perú', 'Perú'), ('Uruguay', 'Uruguay'),
              ('Venezuela', 'Venezuela'))
    nacionalidad=models.CharField( max_length=20, default='Bolivia')
    puntaje = models.IntegerField(null=True)
    generos=( ('M', 'Masculino'), ('F', 'Femenino'))
    genero = models.CharField(choices=generos, default='FN', max_length=10)
    #descripcion = models.CharField(max_length=140, default='¡Hola mundo!')
    last_login = models.DateTimeField(null=True)
    is_staff = models.BooleanField(null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(null=True)
    last_login = models.DateTimeField(null=True)
    date_joined = models.DateTimeField(null=True)

class Categoria(models.Model):
    nombre = models.CharField(max_length= 30)

class Noticia(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=500)
    fuente = models.CharField(max_length= 100)
    puntaje = models.IntegerField()
    creador = models.ForeignKey(Usuario,null=True, blank=False, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    paises = (('Argentina', 'Argentina'), ('Bolivia', 'Bolivia'), ('Brasil', 'Brasil'),
              ('Chile', 'Chile'), ('Colombia', 'Colombia'), ('Ecuador', 'Ecuador'),
              ('Paraguay', 'Paraguay'), ('Perú', 'Perú'), ('Uruguay', 'Uruguay'),
              ('Venezuela', 'Venezuela'), ('Internacional', 'Internacional'))
    pais = models.CharField(choices=paises, default='Internacional',max_length=20)
    imagen = models.CharField(max_length=100, default='default')
    #categoria = models.ForeignKey(Categoria, default=None, blank=False, on_delete=models.CASCADE)

class Denuncia(models.Model):
    descripcion = models.CharField(max_length=500)
    correo = models.CharField(null=True ,max_length=30)
    #fecha = models.DateTimeField(auto_now_add=True)
    tipos = (('FN', 'Fake New'), ('HS', 'Harassment'), ('H', 'Hate'), ('N', 'Nudes'),
             ('PP', 'Personal Profit'), ('S', 'Spam'), ('SS', 'Suicide or Self-harm'),
             ('T', 'Terrorism'), ('V', 'Violence'), ('S', 'Others'))
    tipo = models.CharField(choices=tipos, default='FN', max_length=30)



