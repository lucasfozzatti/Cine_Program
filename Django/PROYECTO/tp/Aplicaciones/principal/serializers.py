from rest_framework import serializers
from .models import Pelicula, Proyeccion, Sala, Reserva


class PeliculaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pelicula
        fields = ('id',
                  'nombre',
                  'duracion',
                  'descripcion',
                  'detalle',
                  'genero',
                  'clasificacion',
                  'estado',
                  'fechaComienzo',
                  'fechaFinalizacion')


class ProyeccionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proyeccion
        fields = ('id',
                  'fecha_inicio',
                  'fecha_fin',
                  'hora',
                  'estado',
                  'pelicula',
                  'sala')


class SalaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sala
        fields = ('id',
                  'nombre',
                  'estado',
                  'filas',
                  'asientos')


class ReservaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserva
        fields = ('id',
                  'fecha',
                  'filas',
                  'asientos',
                  'proyeccion')
