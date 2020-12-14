from django.shortcuts import render, redirect
from .models import Pelicula
from .forms import PeliculasForm
from django.http import HttpResponse, HttpRequest
from django.core import serializers
import datetime


def inicio(request):
    if request.method == 'GET':
        pelicula = serializers.serialize('json', Pelicula.objects.all())
        
        return HttpResponse(pelicula)


def tabla_rango(request, fecha_inicio, fecha_fin): 
    print("fechas", fecha_inicio, fecha_fin)   
    if request.method == 'GET':
        pelicula = serializers.serialize('json', Pelicula.objects.filter(start_date=fecha_inicio, end_date=fecha_fin))

    return HttpResponse(pelicula)


def tabla_fecha(request):
    if request.method == 'GET':
        
        pelicula = serializers.serialize('json', Pelicula.objects.filter(start_date = datetime.datetime.now()))
        print(pelicula)
        return HttpResponse(pelicula)







def crear_pelicula(request):
    if request.method == "GET":
        
                                            
        form = PeliculasForm()
        contexto = {
            'form':form
        }
    
    else:
        form = PeliculasForm(request.POST)  
        contexto = {
            'form':form
        } 
        if form.is_valid():
            
            return redirect('index')

    return render(request,'create_pelicula.html',contexto)  

   


# Create your views here.
