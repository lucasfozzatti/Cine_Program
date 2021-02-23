from django.shortcuts import render, redirect
from .models import Pelicula, Sala, Proyeccion, Reserva
from rest_framework.decorators import api_view
from django.http import HttpResponse, HttpRequest
from django.core import serializers
import datetime
from .serializers import *
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser

#tabla de todas las peliculas
def inicio(request):
    if request.method == 'GET':
        pelicula = serializers.serialize('json', Pelicula.objects.all())
        
        return HttpResponse(pelicula)

#tabla de las peliculas disponibles en un rango de tiempo
def tabla_rango(request, fecha_inicio, fecha_fin): 
    print("fechas", fecha_inicio, fecha_fin)   
    if request.method == 'GET':
        pelicula = serializers.serialize('json', Pelicula.objects.filter(start_date=fecha_inicio, end_date=fecha_fin))

    return HttpResponse(pelicula)

#tabla con las peliculas disponibles hoy
def tabla_fecha(request):
    if request.method == 'GET':
        pelicula = serializers.serialize('json', Pelicula.objects.filter(start_date = datetime.datetime.now()))
        print(datetime.datetime.now)
        print(pelicula)
        return HttpResponse(pelicula)
#tabla bonita
def tabla(request):
    if request.method == "GET":
        pelicula = Pelicula.objects.all()
                                            
        
        contexto = {
            'pelicula':pelicula
        }
        print(contexto)
    return render(request, 'index.html', contexto) 

##############################################################################    
@api_view(['GET', 'POST'])

def salas(request):
    if request.method == 'GET':
        salas = Sala.objects.all()
        salas_serialazer = SalaSerializer(salas, many=True)
        return JsonResponse(salas_serialazer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        salas_data = JSONParser().parse(request)
        salas_serialazer = SalaSerializer(data=salas_data)
        if salas_serialazer.is_valid():
            salas_serialazer.save()
            return JsonResponse(salas_serialazer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(salas_serialazer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def sala_detalle(request, nombre):
    try:
        sala = Sala.objects.get(nombre=nombre)
    except Sala.DoesNotExist:
        return JsonResponse({'Error': 'La sala no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        sala_serializer = SalaSerializer(sala)
        return JsonResponse(sala_serializer.data, status=status.HTTP_200_OK)

   #.....VER PUT Y DELETE ......
    elif request.method == 'PUT':
                sala_data = JSONParser().parse(request)
                sala_serializer = SalaSerializer(sala, data=sala_data)
                if sala_serializer.is_valid():
                    proyecciones = Proyeccion.objects.filter(sala=sala)
                    if (proyecciones.count() != 0):
                        for proyeccion in proyecciones:
                            if(proyeccion.estado):
                                return JsonResponse({'Mensaje':
                                                    'Sala asociada, deshabilite la proyeccion para editar la sala'})
                    sala_serializer.save()
                    return JsonResponse(sala_serializer.data)
                return JsonResponse(sala_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
            sala.delete()
            return JsonResponse({'Mensaje': 'La sala se elimino correctamente'}, status=status.HTTP_204_NO_CONTENT)
            
@api_view(['GET', 'POST'])

def proyecciones(request):  
    if request.method == 'GET':
        pelicula = serializers.serialize('json', Pelicula.objects.filter(start_date = datetime.datetime.now()))
        print(datetime.datetime.now)
        print(pelicula)
        return HttpResponse(pelicula)
