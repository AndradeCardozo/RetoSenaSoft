from django import forms
from App.models import *
from importlib.resources import contents
from secrets import choice
from tkinter import Widget
from django import forms
from django.core.validators import RegexValidator
from django.contrib.auth.forms import UserCreationForm


from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class Mensajesform(forms.ModelForm):
    file = forms.FileField(required=False)
    estado = forms.CharField(required=False) 
    class Meta:
        model = Mensajes
        fields = '__all__'
        

class UserRegistrationForm(UserCreationForm):
    
    email = forms.CharField(label='Correo electronico', required=False ,widget=forms.TextInput(attrs={'placeholder':'Correo electronico','style':'text-transform: lowercase'}))
    date_joined = forms.DateField(label='Fecha de nacimiento',required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    password1 = forms.CharField(label='Contraseña ',widget=forms.PasswordInput(attrs={'placeholder':'Contraseña','type':'password'}))
    password2 = forms.CharField(label='Confirmar contraseña',widget=forms.PasswordInput(attrs={'placeholder':'Confirmar contraseña','type':'password'}))
    userDocumento = forms.CharField( label='Tipo de documento',widget=forms.Select(choices=UsuarioPerzonalizado.DOCUMENTO))
    
    username = forms.CharField(label='Ingrese su numero de documento', min_length=5, max_length=15, validators=[RegexValidator(regex='^[0-9]*$', message='Solo se permiten numeros.')], 
                        widget=forms.TextInput(attrs={'placeholder': 'Ingrese su numero de Documento', }))
    
    
    userNombreCompleto = forms.CharField(label='Nombre completo',widget=forms.TextInput(attrs={'placeholder':'Nombre completo','style':'text-transform: capitalize'}))
    userApellidos = forms.CharField(label='Apellidos Completos',widget=forms.TextInput(attrs={'placeholder':'Apellidos','style':'text-transform: capitalize'}))
    userSexo = forms.CharField(label='Sexo',widget=forms.Select(choices=UsuarioPerzonalizado.SEXO))
    
    userTelefono = forms.CharField(label='Telefono',widget=forms.TextInput(attrs={'placeholder':'Telefono'}))
    userTelefonoFijo = forms.CharField(label='Telefono fijo',widget=forms.TextInput(attrs={'placeholder':'Telefono fijo'}))
    userCorreo = forms.CharField(label='Correo electronico',widget=forms.TextInput(attrs={'placeholder':'Correo electronico','style':'text-transform: lowercase'})) 
    
    userMunicipio = forms.CharField( label='Municipio',widget = forms.TextInput(attrs={'placeholder':'Municipio','style':'text-transform: capitalize'}))
    userDireccion = forms.CharField(label='Direccion', required=None, widget=forms.TextInput(attrs={'placeholder':'Direccion','style':'text-transform: capitalize'}))
    userBarrio = forms.CharField(label='Barrio - Vereda',widget=forms.TextInput(attrs={'placeholder':'Barrio','style':'text-transform: capitalize'}))
    
    userFechaNacimiento =  forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(attrs={'type': 'date'}))
    userEtnia = forms.CharField(label='Etnia',widget=forms.TextInput(attrs={'placeholder':'Etnia','style':'text-transform: capitalize'}))
    
    userCondicionDiscapacidad =  forms.CharField(label='Condición de discapacidad', max_length=5000, widget=forms.Textarea(attrs={'placeholder': 'Escriba su condicion de discapacidad', 'rows': '5', 'cols': '50'}))
    
    userEstrato = forms.CharField(label='Estrato',widget=forms.NumberInput (attrs={'placeholder':'Estrato','style':'width: 400px; '}))
    
    userUltimoNivelEducativo = forms.CharField(label='Ultimo nivel educativo',widget=forms.TextInput(attrs={'placeholder':'Escriba su ultimo nivel alcanzado','style':'width: 500px'}))
    
    userDispositivo = forms.BooleanField(label='Dispositivo', required=False) 
    userTipoDispositivo = forms.CharField(label='Tipo de dispositivo',widget=forms.Select(choices=UsuarioPerzonalizado.TIPODISPOSITIVO))
    userConectividad =forms.BooleanField(label='¿Cuenta con conectividad a internet?', required=False)
    
    userTipoAfiliacion = forms.CharField(label='Tipo afiliacion', widget=forms.Select(choices=UsuarioPerzonalizado.AFILIACION, attrs={'style ': 'width: 400px'}))
    password = forms.CharField(label='Contraseña',required=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    
    ESTADO =[('0','0'),('1','1')]
    
    is_active = forms.CharField (label='Estado',widget=forms.TextInput(attrs={'value':'1','type':'hidden'}))
    
    class Meta:
        model=UsuarioPerzonalizado
        fields='__all__'
        
class PreguntasForm(forms.ModelForm):

    
    class Meta:
        model = Encuesta
        fields = '__all__'