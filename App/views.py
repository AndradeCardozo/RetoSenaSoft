from cmath import inf
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from App.forms import Mensajesform, PersonaForm
from App.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import auth
from datetime import datetime
from django.contrib.auth import authenticate 

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
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect ('/')
        else:
            return render (request, 'inicio.html', {'form': form})
    else:
        form = PersonaForm()
    return render(request, 'registration/registrar.html', {'form': form})

# Funciones de usuario
@login_required (login_url='/iniciarSesion/')
def ciudadano(request):
    questions = Encuesta.objects.all()
    return render(request, 'ciudadano/principal.html', {'questions': questions})

def buscarPerfil(request, cedula):
    perfil = Sondeo.objects.get(id=cedula)
    return HttpResponseRedirect('/perfil', perfil)


@login_required (login_url='/iniciarSesion/')
def perfil(request, pk):
    persona = Persona.objects.get(id=pk)
    data={
        'persona': persona
    }
    return render(request, 'ciudadano/perfil.html', data)

@login_required (login_url='/iniciarSesion/')
def sondeos(request, pk):
    question = Encuesta.objects.get(id=pk)
    options = question.choices.all()
    return render(request, 'ciudadano/enviarSondeo.html',  {'question':question, 'options': options })
    
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



# def vote(request,pk):
#     question = Sondeo.objects.get(id=pk)
#     options = question.choices.all()
#     # if request.method == 'POST':
#     #     inputvalue = request.POST['choice']
#     #     selection_option = options.get(id=inputvalue)
#     #     selection_option.vote += 5
#     #     selection_option.save()

#     return render(request, '', {'question':question, 'options': options })

# def result(request, pk):
#     question = Sondeo.objects.get(id=pk)
#     options = question.choices.all()
#     if request.method == 'POST':
#         inputvalue = request.POST['choice']
#         selection_option = options.get(id=inputvalue)
#         selection_option.vote += 5
#         selection_option.save()
#     return render(request, '', {'question': question, 'options': options})

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