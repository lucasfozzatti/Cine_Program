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
from Aplicaciones.principal.views import inicio, crear_pelicula, tabla_fecha, tabla_rango
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', inicio, name = 'index'),
    path('create_pelicula/', crear_pelicula, name = 'create_pelicula'),
    url(r'tabla_fecha', tabla_fecha, name='tabla_fecha'),
    url(r'^(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', tabla_rango),
    
]

# urlpatterns = [
#     path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
#     path('', views.index, name='index'),
#     path('butacas/', views.butacas, name='butacas'),
#     url(r'^api/peliculas$', views.pelicula_list),
#     url(r'^api/peliculas/([a-zA-Z0-9 ]+)/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.pelicula_detalle),
#     url(r'^api/peliculas/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.pelicula_fechas),
#     url(r'^api/salas$', views.sala_list),
#     url(r'^api/salas/([a-zA-Z0-9 ]+)$', views.sala_detalle)
#     #url(r'^api/tutorials/(?P<pk>[0-9]+)$'
# ]


