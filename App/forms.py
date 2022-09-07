from django import forms
from App.models import *
from importlib.resources import contents
from secrets import choice
from tkinter import Widget
from django import forms
from django.core.validators import RegexValidator

class Mensajesform(forms.ModelForm):
    file = forms.FileField(required=False)
    estado = forms.CharField(required=False) 
    class Meta:
        model = Mensajes
        fields = '__all__'
        


class PersonaForm(forms.ModelForm):
    
    perDocumento = forms.CharField( label='Tipo de documento',widget=forms.Select(choices=Persona.DOCUMENTO))
    perNumeroDocumento = forms.CharField(label='Numero de documento',widget=forms.TextInput(attrs={'placeholder':'Numero de documento'}))
    perNombreCompleto = forms.CharField(label='Nombre completo',widget=forms.TextInput(attrs={'placeholder':'Nombre completo','style':'text-transform: capitalize'}))
    perApellidos = forms.CharField(label='Apellidos Completos',widget=forms.TextInput(attrs={'placeholder':'Apellidos','style':'text-transform: capitalize'}))
    perSexo = forms.CharField(label='Sexo',widget=forms.Select(choices=Persona.SEXO))
    
    perTelefono = forms.CharField(label='Telefono',widget=forms.TextInput(attrs={'placeholder':'Telefono'}))
    perTelefonoFijo = forms.CharField(label='Telefono fijo',widget=forms.TextInput(attrs={'placeholder':'Telefono fijo'}))
    perCorreo = forms.CharField(label='Correo electronico',widget=forms.TextInput(attrs={'placeholder':'Correo electronico','style':'text-transform: lowercase'})) 
    
    perMunicipio = forms.CharField( label='Municipio',widget = forms.TextInput(attrs={'placeholder':'Municipio','style':'text-transform: capitalize'}))
    perDireccion = forms.CharField(label='Direccion', required=None, widget=forms.TextInput(attrs={'placeholder':'Direccion','style':'text-transform: capitalize'}))
    perBarrio = forms.CharField(label='Barrio - Vereda',widget=forms.TextInput(attrs={'placeholder':'Barrio','style':'text-transform: capitalize'}))
    
    perFechaNacimiento =  forms.DateField(label='Fecha de nacimiento', widget=forms.DateInput(attrs={'type': 'date'}))
    perEtnia = forms.CharField(label='Etnia',widget=forms.TextInput(attrs={'placeholder':'Etnia','style':'text-transform: capitalize'}))
    
    perCondicionDiscapacidad =  forms.CharField(label='Condición de discapacidad', max_length=5000, widget=forms.Textarea(attrs={'placeholder': 'Escriba su condicion de discapacidad', 'rows': '5', 'cols': '50'}))
    
    perEstrato = forms.CharField(label='Estrato',widget=forms.NumberInput (attrs={'placeholder':'Estrato','style':'width: 400px; '}))
    
    perUltimoNivelEducativo = forms.CharField(label='Ultimo nivel educativo',widget=forms.TextInput(attrs={'placeholder':'Escriba su ultimo nivel alcanzado','style':'width: 500px'}))
    
    perDispositivo = forms.BooleanField(label='Dispositivo', required=False) 
    perTipoDispositivo = forms.CharField(label='Tipo de dispositivo',widget=forms.Select(choices=Persona.TIPODISPOSITIVO))
    perConectividad =forms.BooleanField(label='¿Cuenta con conectividad a internet?', required=False)
    
    perTipoAfiliacion = forms.CharField(label='Tipo afiliacion', widget=forms.Select(choices=Persona.AFILIACION, attrs={'style ': 'width: 400px'}))
    
    class Meta:
        model = Persona
        fields = '__all__'