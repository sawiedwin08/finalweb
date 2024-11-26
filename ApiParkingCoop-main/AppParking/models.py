from enum import unique

from django.contrib.auth.models import AbstractUser
from django.db import models

class Parqueadero(models.Model):
    nombre = models.CharField(max_length=100,null=False,unique=True)
    nit = models.IntegerField()
    direccion = models.CharField(max_length=100,null=False)
    telefono = models.CharField(max_length=10,null=False)
    capacidad_total = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Usuario(AbstractUser):
    parqueadero = models.ForeignKey(Parqueadero,null=True, on_delete=models.PROTECT)
    direccion = models.CharField(max_length=100,null=False)
    telefono = models.CharField(max_length=100,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Tarifa(models.Model):
    parqueadero = models.ForeignKey(Parqueadero,on_delete = models.PROTECT)
    tamano = models.CharField(max_length=100,null=False)
    precio = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Propietario(models.Model):
    nombres = models.CharField(max_length=100,null=False)
    identificacion = models.CharField(max_length=12,null=False,unique=True)
    email = models.EmailField(null=False)
    edad = models.IntegerField(default=18)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Vehiculo(models.Model):
    propietario = models.ForeignKey(Propietario,on_delete = models.PROTECT)
    parqueadero = models.ForeignKey(Parqueadero,on_delete = models.PROTECT)
    placa = models.CharField(max_length=8,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EntradaSalida(models.Model):
    tarifa = models.ForeignKey(Tarifa,on_delete = models.PROTECT)
    vehiculo = models.ForeignKey(Vehiculo,on_delete = models.PROTECT)
    usuario = models.ForeignKey(Usuario,on_delete = models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)







