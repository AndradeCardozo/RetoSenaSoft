from cmath import inf
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from App.forms import Mensajesform, PreguntasForm, UserRegistrationForm
from App.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import auth
from datetime import datetime
from django.contrib.auth import authenticate

from .utils import render_to_pdf
from django.http import HttpResponse
#
from django.views.generic import View


# Create your views here.

# =======================FRONTEND=============================

# Funcion para ir a la pagina principal (frontend)

def iniciarSesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if user.is_superuser:
                return redirect('/admin')
            else:
                return redirect ('/ciudadano')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
            return redirect('/iniciarSesion')
    return render(request, 'registration/login.html')


def cerrarSesion (request):
    auth.logout(request)
    return redirect('/')

def home(request):
    # form = Costumerform()
    return render(request, 'home.html')

@login_required (login_url='/iniciarSesion/')
def send_message(request):
    if request.method == "POST":
        form = Mensajesform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mensaje enviado')
            return HttpResponseRedirect('/')
        else:
            print("hola")
            return render(request, 'home.html', {'form': form})
    else:
        form = Mensajesform()
    return render(request, 'home.html', {'form': form})

# Registrarse
def registrar(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST) 
        if form.is_valid():
            form.save()
            messages.success(request, "Ususario registrado correctamente" )
            return HttpResponseRedirect ('/iniciarSesion')
        else:
            messages.error(request, 'Error al registrar usuario')
            return render (request, 'registration/registrar.html', {'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/registrar.html', {'form': form ,})


# Funciones de usuario
@login_required (login_url='/iniciarSesion/')
def ciudadano(request):
    questions = Encuesta.objects.all()
    return render(request, 'ciudadano/principal.html', {'questions': questions})

def buscarPerfil(request, cedula):
    perfil = Sondeo.objects.get(id=cedula)
    return HttpResponseRedirect('/perfil', perfil)


# @login_required (login_url='/iniciarSesion/')



@login_required (login_url='/iniciarSesion/')
def encuesta(request):
    questions = Sondeo.objects.all()
    return render(request, 'ciudadano/versondeos.html', {'questions':questions})

def perfil(request):    
    return render(request, 'ciudadano/perfil.html')

def actualizar(request, pk):
    casa = Encuesta.objects.get(id=pk)
    if request.method == "POST":
        form = PreguntasForm(request.POST, instance=casa)
        if form.is_valid(): 
            form.save()
            pdf = render_to_pdf('pdf/lista.html')
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            form = PreguntasForm()
            # return render(request, 'home.html', {'form': form})
    else:
        form = PreguntasForm()
        
    return HttpResponseRedirect('/encuesta', form)

@login_required (login_url='/iniciarSesion/')
def preguntas(request, pk):
    projects = Sondeo.objects.filter(encuesta= pk)
    valores = []
    i = 0
    for project in projects: 
        developers = project.encuesta.all()
        valores.append(project)
        print(valores)
        print(developers)
        print(projects)
        print(project)
        print(i)
        

        form = PreguntasForm()
            

            
            
    data={
        'valores':valores,
        'developers':developers,
        'form': form,
    }
    return render(request, 'ciudadano/enviarSondeo.html',data)
    
def enviarEncuesta(request):  
    # if request.method == "POST":
    #     form = PreguntasForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Mensaje enviado')
    #         return HttpResponseRedirect('/')
    #     else:
    #         print("hola")
    #         return render(request, 'home.html', {'form': form})
    # else:
    #     form = PreguntasForm()
    return HttpResponseRedirect('/home')
    
@login_required (login_url='/iniciarSesion/')
def sondeosrealizados(request, pk):
    question = Encuesta.objects.get(id=pk)
    options = question.choices.all()
    if request.method == 'POST':
        inputvalue = request.POST['choice']
        selection_option = options.get(id=inputvalue)
        selection_option.vote += 5
        selection_option.save()
    return render(request, 'ciudadano/consultarSondeo.html', {'question':question, 'options': options })



# =======================BACKEND=============================
 
# Funcion de login
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

# Funcion para retornar pagina de inbox

@login_required (login_url='/iniciarSesion/')
def inbox(request):
    if 'q' in request.GET:
        q = request.GET['q']
        all_customer_list = Mensajes.objects.filter(
            Q(name__icontains=q) | Q(phone__icontains=q) |
            Q(email=q) | Q(subject__icontains=q) |
            Q(message__icontains=q) | Q(estado__icontains=q)
        ).order_by('-created_at')
    else:
        all_customer_list = Mensajes.objects.all().order_by('-created_at')
    paginator = Paginator(all_customer_list, 3)
    page = request.GET.get('page')
    all_customer = paginator.get_page(page)
    
    # -------------------Mensaje al container---------------------------
    # 1) total
    total = Mensajes.objects.all().count()
    # 2) Read
    read  = Mensajes.objects.filter(estado='Read').count()
    # 3) Unread
    pending = Mensajes.objects.filter(estado='Pending').count()
    # 4) Today
    base = datetime.now().date()
    today = Mensajes.objects.filter(created_at__gt = base)
    
    data={
        'mensajes':all_customer,
        'total':total,
        'read':read,
        'pending':pending,
        'today':today
    }
    return render(request, 'admin/mensajes.html', data)

# Funcion para eliminar
@login_required (login_url='/iniciarSesion/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_message(request, customer_id):
    customer = Mensajes.objects.get(id=customer_id)
    customer.delete()
    messages.success(request, 'Registro eliminado')
    return HttpResponseRedirect('/inbox')


# class ListEmpleadosPdf(View):
#     def get(self, request, *args, **kwargs):
#         empleados = UsuarioPerzonalizado.objects.all()
#         data = {
#             'count': empleados.count(),
#             'empleados': empleados
#         }
#         pdf = render_to_pdf('home/lista.html', data)
#         return HttpResponse(pdf, content_type='application/pdf')