"""tp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Aplicaciones.principal.views import *
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/all_movies', all_movies, name='salas'),
    url(r'^api/peliculas/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', traer_peliculas),
    url(r'^api/rango/([a-zA-Z0-9 ]+)/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', tabla_rango),
    url(r'^api/salas', salas, name='salas'),
    url(r'^api/sala_detalle/([a-zA-Z0-9 ]+)$', sala_detalle),
    url(r'^api/tabla$', tabla, name='tabla'),
    url(r'^api/proyecciones$', proyecciones),
    url(r'^api/proyecciones_rango/(\d{4}[-/]\d{2}[-/]\d{2})$', proyecciones_rango, name='proyecciones_rango'),
    url(r'^api/proyeccion_info/([a-zA-Z0-9 ]+)/(\d{4}[-/]\d{2}[-/]\d{2})$', proyeccion_info),
    url(r'^api/butacas_all$', butacas_all),
    url(r'^api/proyeccion_new/([a-zA-Z0-9 ]+)$', proyeccion_new),
    url(r'^api/butaca_reservada/([a-zA-Z0-9 ]+)$', butaca_reservada),
    url(r'^api/butacas_vendidas/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', butacas_vendidas),
    url(r'^api/butacas_proyeccion/([a-zA-Z0-9 ]+)/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', butacas_proyeccion),
    url(r'^api/butacas_ranking/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', butacas_ranking),
    url(r'^api/entradas_totales$', entradas_totales),
    url(r'^api/peliculas_service$', peliculas_service),
    
    ]



