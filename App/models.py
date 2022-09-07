from django.db import models
from django.utils.html import format_html
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from re import T

# Create your models here.
STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("Read", "Read"),
)


class Mensajes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    message = models.TextField(max_length=1001)
    file = models.FileField(upload_to='foto')
    created_at = models.DateTimeField(auto_now_add=True)
    estado = models.CharField( 
        max_length = 20, 
        choices = STATUS_CHOICES, 
        default = 'Pending'
        ) 
    
    # control de respuesta leidas/no leidas
    def situation(self):
        if self.estado == 'Read':
            return format_html('<span style="color:green">{0}</span>', self.estado)
        else:
            return format_html('<span style="color:red">{0}</span>', self.estado)
    situation.allow_tags = True
    
    def __str__(self):
        return self.name
    
class Persona (models.Model):
    
    DOCUMENTO = [
        ('Cedula de ciudadania','Cedula de ciudadania'),
        ('Tarjeta de identidad','Tarjeta de identidad'),
        ('Cédula de extranjería','Cédula de extranjería')
    ]
    
    SEXO = [
        ('Hombre','Hombre'),
        ('Mujer','Mujer'),
        ('Intersexual','Intersexual'),
        ('Indefinido','Indefinido'),
        ('Prefieren no decir','Prefieren no decir'),

    ] 
    DISPOSITIVO =[
        ('Si','Si'),
        ('No','No'),
    ]
    
    TIPODISPOSITIVO= [
        ('T. Móvil','T. Móvil'),
        ('Computador','Computador'),
        ('Tablet','Tablet'),
        ('Otro','Otro'),
    ]
    
    AFILIACION = [
        ('Subsidiado','Subsidiado'),
        ('contributivo','contributivo'),
    ]
    
    perDocumento = models.CharField (max_length=200,choices= DOCUMENTO )
    perNumeroDocumento = models.CharField (max_length=12,) 
    perNombreCompleto = models.CharField (max_length=20)
    perApellidos = models.CharField (max_length=30,)
    perSexo = models.CharField (max_length=20,choices = SEXO)
    
    #CONTACTO
    perTelefono = models.CharField (max_length=11)
    perTelefonoFijo = models.CharField (max_length=11)
    perCorreo = models.EmailField (max_length=20)
    
    
    #GEOGRAFICA
    perMunicipio = models.CharField (max_length=10)
    perDireccion = models.CharField (max_length=30,null=True,blank=True)
    perBarrio = models.CharField (max_length=100)
    
    #ENFOQUE DIRECENCIAL
    perFechaNacimiento = models.DateField (auto_now=False, auto_now_add=False)
    perEtnia =models.CharField (max_length=30)
    
    #ENFOQUE POBLACIONAL
    perCondicionDiscapacidad = models.CharField (max_length=60)
    
    #SOCIOECONOMICO
    perEstrato = models.CharField (max_length=3)
    
    #ESCOLARIDAD 
    perUltimoNivelEducativo = models.CharField (max_length=25)
    
    #ACCESO Y CONECTIVIDAD A MEDIOS TECNOLOGICOS
    perDispositivo = models.BooleanField (max_length=100,default=False)
                                         
    perTipoDispositivo = models.CharField (max_length=100,choices=TIPODISPOSITIVO)
    perConectividad = models.BooleanField (max_length=100,default=False)
    
    #SALUD
    perTipoAfiliacion = models.CharField (choices= AFILIACION ,max_length=100)
    
    class Meta:
        db_table = 'persona'
    
    def __str__(self):
        return self.perNumeroDocumento 
class Sondeo (models.Model):
    
    TIPOSONDEO = [
        ('Pregunta','Pregunta'),
        ('Fecha','Fecha'),
        ('Opciones de respuesta','Opciones de respuesta'),    
    ]
    
    sonTipo = models.CharField (choices=TIPOSONDEO, max_length=100)
    sonTitulo = models.CharField (max_length=100)
    sonFechaApertura = models.DateField (auto_now=False, auto_now_add=False)
    sonHoraApertura = models.TimeField (auto_now=False, auto_now_add=False)
    sonFechaCierre = models.DateField (auto_now=False, auto_now_add=False)
    sonHoraCierre = models.TimeField (auto_now=False, auto_now_add=False)
    sonPersona = models.ForeignKey (Persona, on_delete=models.CASCADE)
    sonRespuesta = models.CharField (max_length=100)
    sonObservaciones = models.CharField (max_length=100)    
    
    class Meta:
        db_table ='sondeo'
    