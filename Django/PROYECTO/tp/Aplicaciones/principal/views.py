from django.shortcuts import render, redirect
from .models import Pelicula, Sala, Proyeccion, Reserva
from rest_framework.decorators import api_view
from django.http import HttpResponse, HttpRequest
from django.core import serializers
import datetime
from .serializers import PeliculaSerializer, ProyeccionSerializer, SalaSerializer, ReservaSerializer
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from django.db.models import Q
from django.core.exceptions import PermissionDenied
import datetime as dt
import urllib
import json
import dateutil.parser


@api_view(['GET'])
def tabla(request):
    if request.method == "GET":
        pelicula = Pelicula.objects.all()
                                            
        contexto = {
            'pelicula':pelicula
        }
        
    return render(request, 'index.html', contexto) 


@api_view(['GET', 'POST','PUT'])
def all_movies(request):
    if request.method == 'GET':
        peliculas = Pelicula.objects.all()
        peliculas_serializer = PeliculaSerializer(peliculas, many=True)
        
        return JsonResponse(peliculas_serializer.data, safe=False, status=status.HTTP_200_OK)



@api_view(['GET'])
def traer_peliculas(request, fecha_inicio, fecha_fin):
    if request.method == 'GET':

        peliculas = Pelicula.objects.filter((Q(fechaComienzo__lte=fecha_fin) & Q(fechaFinalizacion__gte=fecha_inicio))|(Q(fechaComienzo__lte=fecha_inicio) & Q(fechaComienzo__gte=fecha_inicio)) |
        (Q(fechaFinalizacion__gte=fecha_fin) & Q(fechaFinalizacion__lte=fecha_fin)
        ))

        peliculas_serializer = PeliculaSerializer(peliculas, many=True)

        return JsonResponse(peliculas_serializer.data, safe=False, status=status.HTTP_200_OK)
    else:    
        return JsonResponse({'mensaje': 'No hay peliculas'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def tabla_rango(request,id, fecha_inicio, fecha_fin): 

    pelicula = Pelicula.objects.get(id=id)
    proyeccion = Proyeccion.objects.filter(fecha_inicio__lte=fecha_fin, fecha_fin__gte=fecha_inicio, pelicula=id)
   
    if request.method == 'GET':
        fechas = []
        

        for i in proyeccion:
            fechas.append(i.fecha_inicio)

        
        peliculas_serializer = PeliculaSerializer(pelicula)
        
        Dic = {}
        Dic.update(peliculas_serializer.data)
        Dic["Fechas"] = fechas
        
        if peliculas_serializer != "":
            return JsonResponse(Dic, status=status.HTTP_200_OK) 
        else:       
            return JsonResponse({'mensaje': 'No hay peliculas'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'POST','PUT'])
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



@api_view(['GET', 'POST','DELETE','PUT'])
def sala_detalle(request, id):
   
    try:
        sala = Sala.objects.get(id=id)
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

    elif request.method == 'DELETE': 
        sala.delete()
        return JsonResponse({'Hecho': 'La sala ha sido eliminada satisfactoriamente!'}, status=status.HTTP_204_NO_CONTENT)

#### proyecciones #####
@api_view(['GET', 'POST'])

def proyecciones(request):  
    
    if request.method == 'GET':
        
        proyecciones = Proyeccion.objects.filter(fecha_inicio__gte =datetime.date.today(), fecha_inicio__lte=datetime.date.today())
        
        proyeccion_serializer = ProyeccionSerializer(proyecciones, many=True)

        return JsonResponse(proyeccion_serializer.data, safe=False, status=status.HTTP_200_OK)

@api_view(['GET', 'POST'])
# proyecciones en cierta fecha
def proyecciones_rango(request, fecha):  
    
    try:
        proyecciones = Proyeccion.objects.filter(fecha_inicio = fecha)
        
        if request.method == 'GET':
            respuesta=[]
            for proyeccion in proyecciones:
                
                respuesta.append({
                    'Proyeccion': proyeccion.id,
                    'Pelicula': proyeccion.pelicula.nombre,
                    'Sala':proyeccion.sala.nombre,
                    'Hora':proyeccion.hora,
                })
           
            return JsonResponse(respuesta, safe=False, status=status.HTTP_200_OK)

    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'La Proyeccion no existe'}, status=status.HTTP_404_NOT_FOUND)   


@api_view(['GET', 'POST','PUT'])

def proyeccion_info(request, id, fecha):
    try:
        reservas = Reserva.objects.filter(fecha=fecha)
        if reservas.count() == 0:

            return JsonResponse({'Mensaje': 'No hay reservas para esta proyeccion'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            butacas = ()
            peli=''
            proyeccion = Proyeccion.objects.filter(pelicula=id, fecha_inicio__gte=fecha, fecha_fin__lte=fecha)
            for i in proyeccion:
                peli=i.pelicula.nombre

            for reserva in reservas:
                
                butacas += "Fila {}, Asiento {}".format(reserva.filas, reserva.asientos),
                respuesta = {
                    'pelicula':peli,
                    'sala':reserva.proyeccion.sala.nombre,
                    'hora':reserva.proyeccion.hora,
                    'butacas reservadas':butacas,
                    
                }
            
            return JsonResponse(respuesta, status=status.HTTP_200_OK)

    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'La Proyeccion no existe'}, status=status.HTTP_404_NOT_FOUND)   

        

@api_view(['POST','PUT'])
def proyeccion_new(request, id):
    try:
        sala = Proyeccion.objects.all()
    except Sala.DoesNotExist:
        return JsonResponse({'Error': 'La reserva no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        sala_post = JSONParser().parse(request)
        pelicula = Pelicula.objects.values("fechaComienzo", "fechaFinalizacion").get(id=sala_post["pelicula"])
        #Comprueba que cuando creo proyeccion se ubique en el rango de la pelicula
        fecha1 = dateutil.parser.parse(sala_post["fecha_inicio"]).date()
        fecha2 = dateutil.parser.parse(sala_post["fecha_fin"]).date()
        fecha_C = dateutil.parser.parse(str(pelicula["fechaComienzo"])).date()

        fecha_F = dateutil.parser.parse(str(pelicula["fechaFinalizacion"])).date()
        print("hola", fecha_F, fecha1)
        if fecha_C >= fecha1 and fecha_F <= fecha2:
            return JsonResponse({'Error': 'Fecha fuera de rango'}, status=status.HTTP_400_BAD_REQUEST)
            
        
        proyeccion_serialazer = ProyeccionSerializer(data=sala_post)
        if proyeccion_serialazer.is_valid():
            proyeccion_serialazer.save()
            return JsonResponse(proyeccion_serialazer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(proyeccion_serialazer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        sala = Proyeccion.objects.get(id=id) 
        sala_put = JSONParser().parse(request)
        proyeccion_serialazer = ProyeccionSerializer(sala, data=sala_put)
        if proyeccion_serialazer.is_valid():
            proyeccion_serialazer.save()
            return JsonResponse(proyeccion_serialazer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(proyeccion_serialazer.errors, status=status.HTTP_400_BAD_REQUEST)
   

@api_view(['GET','POST'])
def butacas_all(request):
    if request.method == 'GET':
    
        butacas = Reserva.objects.all()
        butacas_serializer = ReservaSerializer(butacas, many=True)
        return JsonResponse(butacas_serializer.data, safe=False, status=status.HTTP_200_OK)

    if request.method == 'POST':
        butaca_p = JSONParser().parse(request)
        serializer = ReservaSerializer(data=butaca_p)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        


@api_view(['GET','PUT'])
def butaca_reservada(request, id):

    try:
        butaca = Reserva.objects.get(id=id)
    except Sala.DoesNotExist:
        return JsonResponse({'Error': 'La sala no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        Reserva_serializer = ReservaSerializer(butaca)
        return JsonResponse(Reserva_serializer.data, safe=False, status=status.HTTP_200_OK)

    if request.method == 'PUT': 
        butaca_p = JSONParser().parse(request) 
        butaca_serializer = ReservaSerializer(butaca, data=butaca_p) 
        if butaca_serializer.is_valid(): 
            butaca_serializer.save() 
            return JsonResponse(butaca_serializer.data, status=status.HTTP_200_OK) 
        return JsonResponse(butaca_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### butacas post y put #######

api_view(['POST', 'PUT','GET'])
def butacas_vendidas(request, fecha_inicio, fecha_fin):
    
    try:
        butacas = Reserva.objects.all()
    except Reserva.DoesNotExist:
        return JsonResponse({'mensaje': 'No hay reservas '}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        butacas = Reserva.objects.filter(
        (Q(fecha__lte=fecha_fin) & Q(fecha__gte=fecha_inicio))|(Q(fecha__lte=fecha_inicio) & Q(fecha__gte=fecha_inicio)) |
        (Q(fecha__gte=fecha_fin) & Q(fecha__lte=fecha_fin))
    )
        
    if butacas.count() == 0:
        return JsonResponse({'mensaje': 'No hay peliculas en este rango'}, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        butaca_serializer = ReservaSerializer(butacas, many=True)

        return JsonResponse(butaca_serializer.data, safe=False, status=status.HTTP_200_OK)    


api_view(['POST', 'PUT'])
def butacas_proyeccion(request, id, fecha_inicio, fecha_fin):

    try:
        proyeccion = Proyeccion.objects.get(id=id)
        
        if request.method == 'GET':
    
            butacas = Reserva.objects.filter(fecha__gte=fecha_inicio, fecha__lte=fecha_fin, proyeccion=proyeccion)
            cantidad_butacas = butacas.count()
            respuesta = {
                'Proyeccion': proyeccion.id,
                'Pelicula': proyeccion.pelicula.nombre,
                'Cantidad de butacas vendidas': cantidad_butacas
            }
            return JsonResponse(respuesta, status=status.HTTP_200_OK)

    except Proyeccion.DoesNotExist:
        return JsonResponse({'Mensaje': 'La Proyeccion no existe'}, status=status.HTTP_404_NOT_FOUND)   
    
@api_view(['GET'])
def butacas_ranking(request, fecha_inicio, fecha_fin):
    if request.method == 'GET':

        proyecciones = Proyeccion.objects.filter(fecha_inicio__lte=fecha_fin, fecha_fin__gte=fecha_inicio)
        ranking = []
        for proyeccion in proyecciones:
            butacas = Reserva.objects.filter(proyeccion=proyeccion, fecha__gte=fecha_inicio, fecha__lte=fecha_fin)
            vendidas = butacas.count()
            ranking.append({
                'Pelicula': proyeccion.pelicula.nombre,
                'Butacas vendidas': vendidas
            })
        respuesta = sorted(ranking, key=lambda k: k['Butacas vendidas'], reverse=True)
        respuesta = respuesta[:5]

        return JsonResponse(respuesta, safe=False, status=status.HTTP_200_OK)
    
@api_view(['GET'])
def entradas_totales(request):
   

    if request.method == 'GET':
        peliculas = Pelicula.objects.filter(fechaFinalizacion__gte=dt.date.today(), fechaComienzo__lte=dt.date.today())
        respuesta = []
        
        for pelicula in peliculas:
            total = 0
            proyecciones = Proyeccion.objects.filter(pelicula=pelicula)
            for proyeccion in proyecciones:
                butacas = Reserva.objects.filter(proyeccion=proyeccion, fecha__lte=datetime.datetime.now())
                total += butacas.count()
            respuesta.append({
                'Pelicula': pelicula.nombre,
                'Fecha :{} Vendidas:'.format(datetime.datetime.now()): total,
            })

        return JsonResponse(respuesta, safe=False, status=status.HTTP_200_OK)

@api_view(['POST'])
def peliculas_service(request):
    
    if request.method == 'POST':
        url = "http://localhost:8001/api/pelicula/"
        response = urllib.request.urlopen(url)
        datas = json.loads(response.read())
        
        for peli in datas:
            pelicula = PeliculaSerializer(data=peli)
            if pelicula.is_valid():
                pelicula.save()
            else:
                return JsonResponse({'mensaje': 'Error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse({'mensaje':'Cargado'}, safe=False, status=status.HTTP_200_OK)