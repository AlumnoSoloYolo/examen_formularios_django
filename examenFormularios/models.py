from django.db import models
from django.utils import timezone

# Create your models here.
class Biblioteca(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField(max_length=255)

    def __str__(self):
        return self.nombre
    
class Autor(models.Model):
    nombre = models.CharField(max_length=100, required=True)
    apellidos = models.CharField(max_length=100)
    edad = models.IntegerField(blank=True)


class Libro(models.Model):
    IDIOMAS = [
        ("ES", "Español"),
        ("EN", "Inglés"),
        ("FR", "Francés"),
        ("IT", "Italiano"),
    ]

    nombre = models.CharField(max_length=100)
    idioma = models.CharField(
        max_length=2,
        choices=IDIOMAS,
        default="ES",
    )
    descripcion = models.TextField()
    fecha_actualizacion = models.DateTimeField(default=timezone.now)
    biblioteca = models.ForeignKey(Biblioteca, on_delete=models.CASCADE, related_name="libros_biblioteca")
    autor = models.ManyToManyField(Autor, related_name="libros_autores")


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.CharField(max_length=200,unique=True)
    puntos = models.FloatField(default=5.0,db_column = "puntos_biblioteca")
    libros = models.ManyToManyField(Libro, through='Prestamos', related_name='prestamos_libros')


class DatosCliente(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    direccion = models.TextField()
    gustos = models.TextField()
    telefono = models.IntegerField()

class Prestamo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_prestamo = models.DateTimeField(default=timezone.now)






    

