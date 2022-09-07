from cmath import inf
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from App.forms import Mensajesform, PersonaForm
from App.models import *
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime

# Create your views here.

# =======================FRONTEND=============================

# Funcion para ir a la pagina principal (frontend)
def home(request):
    # form = Costumerform()
    return render(request, 'home.html')

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
def ciudadano(request):
    return render(request, 'ciudadano/principal.html')

def perfil(request):
    return render(request, 'ciudadano/perfil.html')

def sondeos(request):
    return render(request, 'ciudadano/enviarSondeo.html')
    
def sondeosrealizados(request):
    return render(request, 'ciudadano/consultarSondeo.html')
# =======================BACKEND=============================
 
# Funcion de login
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)

# Funcion para retornar pagina de inbox
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
@login_required(login_url="login")
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_message(request, customer_id):
    customer = Mensajes.objects.get(id=customer_id)
    customer.delete()
    messages.success(request, 'Registro eliminado')
    return HttpResponseRedirect('/inbox')