from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Pelicula(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length=70, blank=False, unique = True)
    duracion = models.IntegerField()  # Duracion en minutos
    descripcion = models.CharField(max_length=200, default=False)  # descripcion breve
    detalle = models.CharField(max_length=200)
    genero = models.CharField(max_length=30)
    clasificacion = models.CharField(max_length=5)
    estado = models.BooleanField(default=False)
    fechaComienzo = models.DateTimeField()
    fechaFinalizacion = models.DateTimeField()
    
        
    def __str__(self):
        
        return str(self.nombre)
         

class Sala(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length=70, blank=False)
    estado= models.BooleanField(default=False)
    filas = models.IntegerField()
    asientos = models.IntegerField()

    def __str__(self):
        return self.nombre


class Proyeccion(models.Model):
    id = models.AutoField(primary_key = True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    hora = models.TimeField()   # Hora de proyeccion
    estado= models.BooleanField(default=False)
    def __str__(self):
        return str(self.pelicula)

class Reserva(models.Model):
    id = models.AutoField(primary_key = True)
    proyeccion = models.ForeignKey(Proyeccion, on_delete=models.CASCADE)
    fecha = models.DateField()
    filas = models.IntegerField()
    asientos = models.IntegerField()
    def __str__(self):
        return str(self.proyeccion)

