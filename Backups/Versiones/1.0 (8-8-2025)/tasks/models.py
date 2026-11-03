from djongo import models
from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser

class Reporte(models.Model):
    # Campos existentes
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Nuevos campos
    fecha = models.CharField(max_length=100) 
    folio = models.CharField(max_length=100)
    clave = models.CharField(max_length=100)
    administrador = models.CharField(max_length=100)
    operador = models.CharField(max_length=100)
    damage_vehiculo = models.CharField(max_length=1000)
    damage_bus = models.CharField(max_length=1000)
    damage_others = models.CharField(max_length=1000)
    damage_others2 = models.CharField(max_length=1000)
    damage_others3 = models.CharField(max_length=1000)
    ubicacion = models.CharField(max_length=1000)
    observaciones = models.TextField()
    responsabilidad = models.TextField()
    intervino = models.TextField()
    imagen1 = models.ImageField(upload_to='reportes/', blank=True, null=True)
    imagen2 = models.ImageField(upload_to='reportes/', blank=True, null=True)
    imagen3 = models.ImageField(upload_to='reportes/', blank=True, null=True)
    imagen4 = models.ImageField(upload_to='reportes/', blank=True, null=True)
    imagen5 = models.ImageField(upload_to='reportes/', blank=True, null=True)
    imagen6 = models.ImageField(upload_to='reportes/', blank=True, null=True)

    def __str__(self):
        return self.folio