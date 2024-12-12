from django.db import models
from django.utils import timezone

# Create your models here.

class Usuario(models.Model):    
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    puede_tener_promociones = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
    

class Promocion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(max_length=255)
    activa = models.BooleanField(default=False)
    usuarios = models.ManyToManyField(Usuario, related_name="promo_usuario")
    inicio_promo = models.DateField()
    fin_promo = models.DateField()
    descuento = models.IntegerField()
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="promo_producto")

    
    






    

