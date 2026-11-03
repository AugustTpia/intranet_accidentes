#from djongo import models
from django.db import models
from django import forms
import json
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

class Reporte(models.Model):
    #GENERALES
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    # Listado
    fecha = models.CharField(max_length=100) 
    folio = models.CharField(max_length=100)
    clave = models.CharField(max_length=100)
    administrador = models.CharField(max_length=100)
    ruta = models.TextField()
    operador = models.CharField(max_length=100)
    damage_vehiculo = models.CharField(max_length=1000)
    damage_bus = models.CharField(max_length=1000)
    damage_others = models.CharField(max_length=500)
    damage_others2 = models.CharField(max_length=500)
    damage_others3 = models.CharField(max_length=500)
    ubicacion = models.CharField(max_length=1000)
    costo_finiquito = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    observaciones = models.TextField()
    coordinates = models.TextField(
        blank=True,
        null=True,
        help_text="JSON con las coordenadas del reporte [{id, lat, lng}]"
    )
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
    
    def set_coordinates(self, coordinates_list):
        """ 
        Guarda las coordenadas en formato JSON
        coordinates_list debe ser una lista de diccionarios, example:
        [{ 
            "id": 1,
            "lat": 19.00000,
            "lng": -19.00000
        }]

        json.dumps convierte la lista a una cadena formato JSON
        """
        if coordinates_list:
            self.coordinates = json.dumps(coordinates_list)
        else:
            self.coordinates = None

    def get_coordinates(self):

        """
        Obtiene las coordenadas en formato de lista
        Retorna una lista, ejemplo:
        [{
            "id": 1,
            "lat": 19.000,
            "lng": - 19.000
        }]

        Ó

        []
        """

        if self.coordinates:
            try:
                return json.loads(self.coordinates)
            except json.JSONDecodeError:
                return []
        return []
    
    def get_first_coordinate(self):
        """
        Obtiene la primera coordenada
        Devuelve un diccionario con la primera coordenada, de no existir : None
        """
        coords = self.get_coordinates()
        return coords [0] if coords else None
    
    def has_coordinates(self):
        """Verifica si existen coordenadas al reporte"""

        return bool(self.get_coordinates())
    
    def clean(self):
        if self.coordinates:
            try:
                coords = json.loads(self.coordinates)
                if not isinstance(coords, list):
                    raise ValidationError({'coordinates': 'Las coordenadas deben ser una lista válida'})
                
                # Validar estructura de cada coordenada
                for coord in coords:
                    if not all(key in coord for key in ['id', 'lat', 'lng']):
                        raise ValidationError({'coordinates': 'Cada coordenada debe tener id, lat y lng'})
                    
                    # Validar rangos de latitud y longitud
                    if not (-90 <= coord['lat'] <= 90):
                        raise ValidationError({'coordinates': 'Latitud debe estar entre -90 y 90'})
                    if not (-180 <= coord['lng'] <= 180):
                        raise ValidationError({'coordinates': 'Longitud debe estar entre -180 y 180'})
                        
            except json.JSONDecodeError:
                raise ValidationError({'coordinates': 'Formato JSON inválido para coordenadas'})

    #Listas nombres, en Formulario 
class Lista(models.Model):
    nombre = models.TextField(max_length=100)
    alias = models.TextField(max_length=100)
    comentario = models.TextField(max_length=1000)

    def __str__(self):
        return self.nombre
    
class Administrador(models.Model):
    nombre_Admin = models.CharField(max_length=100)
    alias_Admin = models.CharField(max_length=100)
    comentario_Admin = models.CharField(max_length=1000)

    def __str__(self):
        return self.nombre_Admin
    

class Operador(models.Model):
    nombre_Operador = models.TextField()
    alias_Operador = models.TextField()
    comentario_Operador = models.TextField()

    def __str__(self): 
        return self.nombre_Operador

    