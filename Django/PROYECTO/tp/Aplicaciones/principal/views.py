from django.shortcuts import render, redirect
from .models import Pelicula, Sala, Proyeccion, Reserva
from rest_framework.decorators import api_view
from django.http import HttpResponse, HttpRequest
from django.core import serializers
import datetime
from .serializers import PeliculaSerializer, ProyeccionSerializer, SalaSerializer
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.db.models import Q


@api_view(['GET'])
def tabla(request):
    if request.method == "GET":
        pelicula = Pelicula.objects.all()
                                            
        
        contexto = {
            'pelicula':pelicula
        }
        print(contexto)
    return render(request, 'index.html', contexto) 


@api_view(['GET'])
def traer_peliculas(request):
    if request.method == 'GET':
        peliculas = Pelicula.objects.all()
        peliculas_serializer = PeliculaSerializer(peliculas, many=True)
        return JsonResponse(peliculas_serializer.data, safe=False, status=status.HTTP_200_OK)
    else:    
        return JsonResponse({'mensaje': 'No hay peliculas'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def tabla_rango(request,pk, fecha_inicio, fecha_fin): 

    pelicula = Pelicula.objects.get(pk=pk)
    proyeccion = Proyeccion.objects.filter(
        Q(pelicula=pelicula.id) &
        (Q(start_date__lte=fecha_fin) & Q(end_date__gte=fecha_inicio)) |
        (Q(start_date__lte=fecha_inicio) & Q(start_date__gte=fecha_inicio)) |
        (Q(end_date__gte=fecha_fin) & Q(end_date__lte=fecha_fin))
    )

    print(pelicula)
    
    if request.method == 'GET':
        fechas = []
        proyeccion_serializer = ProyeccionSerializer(proyeccion, many=True)

        for i in proyeccion_serializer.data:
            fechas.append(i['start_date'])

        print(fecha_fin)
        print("fecha_inicio", fecha_inicio)
        
        peliculas_serializer = PeliculaSerializer(pelicula)
        
        newDic = {}
        newDic.update(peliculas_serializer.data)
        newDic["Fechas"] = fechas
        
        if peliculas_serializer != "":
            return JsonResponse(newDic, status=status.HTTP_200_OK) 
        else:       
            return JsonResponse({'mensaje': 'No hay peliculas'}, status=status.HTTP_404_NOT_FOUND)

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


@api_view(['GET','PUT','POST','DELETE'])
def sala_detalle(request, salaId):
    try:
        sala = Sala.objects.get(id=salaId)
    except Sala.DoesNotExist:
        return JsonResponse({'Error': 'La sala no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        sala_serializer = SalaSerializer(sala)
        return JsonResponse(sala_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT': 
        sala_data = JSONParser().parse(request) 
        salas_serializer = SalaSerializer(sala, data=sala_data) 
        if salas_serializer.is_valid(): 
            salas_serializer.save() 
            return JsonResponse(salas_serializer.data, status=status.HTTP_200_OK) 
        return JsonResponse(salas_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'POST':
        salas_data = JSONParser().parse(request)
        salas_serialazer = SalaSerializer(data=salas_data)
        if salas_serialazer.is_valid():
            salas_serialazer.save()
            return JsonResponse(salas_serialazer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(salas_serialazer.errors, status=status.HTTP_400_BAD_REQUEST)
    





        
