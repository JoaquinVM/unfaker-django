from django.db import models
from django.contrib.auth.models import AbstractUser, User
# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class Noticia(models.Model):
    titulo = models.TextField()
    descripcion = models.TextField()
    fuente = models.CharField(max_length=100)
    puntaje = models.FloatField(default=0)
    creador = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='creador')
    fecha = models.DateTimeField(auto_now_add=True)
    paises = (('Argentina', 'Argentina'), ('Bolivia', 'Bolivia'), ('Brasil', 'Brasil'),
              ('Chile', 'Chile'), ('Colombia', 'Colombia'), ('Ecuador', 'Ecuador'),
              ('Paraguay', 'Paraguay'), ('Perú', 'Perú'), ('Uruguay', 'Uruguay'),
              ('Venezuela', 'Venezuela'), ('Internacional', 'Internacional'))
    pais = models.CharField(choices=paises, default='Internacional',max_length=20)
    imagen = models.CharField(max_length=100, default='default')
    categorias = models.ManyToManyField(Categoria)
    usuarios = models.ManyToManyField('Usuario', related_name='usuarios')
    n = models.FloatField(default=2)

    def __str__(self):
        return self.titulo

    def parrafos(self):
        return self.descripcion.split("\n")

    def getPuntaje(self):
        return "%.1f" % self.puntaje

    def getFecha(self):
        return self.fecha.strftime("%d/%m")

    def getYear(self):
        return self.fecha.strftime("%Y")

    def int_puntaje(self):
        return int(round(self.puntaje))

    def rango(self):
        return list(range(self.int_puntaje()))

    def rangoO(self):
        return list(range(5 - self.int_puntaje()))

    def actualizarPuntaje(self, user, voto, punt):
        v = float(voto)
        p = float(punt)
        self.puntaje = self.puntaje + (p/(self.n+p))*(v-self.puntaje)
        self.n += p
        self.usuarios.add(user)
        self.save()


class Denuncia(models.Model):
    descripcion = models.CharField(max_length=500)
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE)
    email = models.CharField(null=True ,max_length=30)
    fecha = models.DateTimeField(null=True, auto_now_add=True)
    tipos = (('FN', 'Fake New'), ('HS', 'Harassment'), ('H', 'Hate'), ('N', 'Nudes'),
             ('PP', 'Personal Profit'), ('S', 'Spam'), ('SS', 'Suicide or Self-harm'),
             ('T', 'Terrorism'), ('V', 'Violence'), ('S', 'Others'))
    tipo = models.CharField(choices=tipos, default='FN', max_length=30)

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
    puntaje = models.FloatField(default=0)
    generos=( ('M', 'Masculino'), ('F', 'Femenino'))
    genero = models.CharField(choices=generos, default='FN', max_length=10)
    descripcion = models.CharField(max_length=140, default='El usuario no ha escrito su descripcion aun.')
    last_login = models.DateTimeField(null=True)
    is_staff = models.BooleanField(null=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(null=True)
    date_joined = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def nacimiento(self):
        if self.fecha_nacimiento:
            return self.fecha_nacimiento.to_python().strftime("%d/%m/%Y")

    def calc_puntaje(self):
        noticias = Noticia.objects.filter(creador=self)
        ns = [noticia.puntaje for noticia in noticias]
        return "%.1f" % (sum(ns)/len(ns))





