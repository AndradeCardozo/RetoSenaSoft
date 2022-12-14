"""inbox URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from App import views# from inbox import settings
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #  =======================ADMIN=============================
    path('admin/', admin.site.urls, name='admin'),
    
    # =======================FRONTEND=============================
    
    path ('iniciarSesion/', views.iniciarSesion, name='iniciarSesion'),
    path  ('cerrarSesion/', views.cerrarSesion, name='logout'),
    path('', views.home, name='home'),
      # Path enviar mensaje
      
    path('send_message', views.send_message, name='send_message'),
    
    # Registar y iniciar
    path('registrar/', views.registrar, name='registrar'), 
    
    # Funciones de usuario
    path('ciudadano/', views.ciudadano, name='ciudadano'),
    path('perfil/', views.perfil, name='perfil'),
    path('sondeos/<str:pk>', views.preguntas, name='sondeos'),
    path('sondeosrealizados/<str:pk>', views.sondeosrealizados, name='sondeosrealizados'),
    path('encuesta/', views.encuesta, name='encuesta'),
    
    path('enviarEncuesta', views.enviarEncuesta, name='enviarEncuesta'),
    # =======================BACKEND=============================
    path('actualizar/<str:pk>', views.actualizar, name='actualizar'),
    path('inbox/', views.inbox, name='inbox'),

    path('delete_message/<str:customer_id>', views.delete_message, name='delete_message'),
    
] 
if settings.DEBUG:
  urlpatterns +=static(
      settings.MEDIA_URL, 
      document_root=settings.MEDIA_ROOT
      )
  
#0b8e02