from django.db import models


# Create your models here.
class Usuario(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    username = models.CharField(max_length=7)
    contrasena = models.CharField(max_length=20)
    email = models.CharField(max_length=10)
    fecha_nacimiento = models.DateField()
    nacionalidad
    puntaje = models.IntegerField()
    genero


class Noticia(models.Model):
    titulo = models.CharField(max_lenght=100)
    descripcion = models.CharField(max_length=500)
    fuente = models.CharField(max_lenght= 00)
    puntaje = models.IntegerField()
    creador = models.ForeignKey(Usuario,null=False, blank=False, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    paises = (('Argentina', 'Argentina'), ('Bolivia', 'Bolivia'), ('Brasil', 'Brasil'),
              ('Chile', 'Chile'), ('Colombia', 'Colombia'), ('Ecuador', 'Ecuador'),
              ('Paraguay', 'Paraguay'), ('Perú', 'Perú'), ('Uruguay', 'Uruguay'),
              ('Venezuela', 'Venezuela'), ('Internacional', 'Internacional'))
    pais = models.CharField(choices=paises, default='Internacional')
    imagen = models.CharField(max_length=100)

class Denuncia(models.Model):
    descripcion = models.CharField(max_length=500)
    fecha = models.DateTimeField(auto_now_add=True)
    tipos = (('FN', 'Fake New'), ('HS', 'Harassment'), ('H', 'Hate'), ('N', 'Nudes'),
             ('PP', 'Personal Profit'), ('S', 'Spam'), ('SS', 'Suicide or Self-harm'),
             ('T', 'Terrorism'), ('V', 'Violence'), ('S', 'Others'))
    tipo = models.CharField(choices=tipos, default='FN')

