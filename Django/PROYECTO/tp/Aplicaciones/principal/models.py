from django.db import models
from django.core.exceptions import ValidationError


class Pelicula(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=70, blank=False, unique = True)
    duration = models.IntegerField()  # Duracion en minutos
    description = models.CharField(max_length=200, default=False)  # descripcion breve
    detail = models.CharField(max_length=200)
    gender = models.CharField(max_length=30)
    classification = models.CharField(max_length=5)
    status = models.CharField(max_length=15)
    start_date = models.DateField()
    end_date = models.DateField()
    
            


    def __str__(self):
        return self.name


class Sala(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=70, blank=False)
    status = models.CharField(max_length=15)
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self):
        return self.name



class Proyeccion(models.Model):
    id = models.AutoField(primary_key = True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    time = models.TimeField()   # Hora de proyeccion
    status = models.CharField(max_length=10)
    def __str__(self):
        return str(self.pelicula)

class Reserva(models.Model):
    id = models.AutoField(primary_key = True)
    proyeccion = models.ForeignKey(Proyeccion, on_delete=models.CASCADE)
    time_r = models.DateField()
    row = models.IntegerField()
    seat = models.IntegerField()


