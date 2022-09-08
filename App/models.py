from django.db import models
from django.utils.html import format_html
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser


class UsuarioPerzonalizado (AbstractUser):
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
    
    userDocumento = models.CharField (max_length=200,choices= DOCUMENTO ) 
    userNombreCompleto = models.CharField (max_length=20)
    userApellidos = models.CharField (max_length=30,)
    userSexo = models.CharField (max_length=20,choices = SEXO)
    
    #CONTACTO
    userTelefono = models.CharField (max_length=11)
    userTelefonoFijo = models.CharField (max_length=11)
    userCorreo = models.EmailField (max_length=20)
    
    
    #GEOGRAFICA
    userMunicipio = models.CharField (max_length=10)
    userDireccion = models.CharField (max_length=30,null=True,blank=True)
    userBarrio = models.CharField (max_length=100)
    
    #ENFOQUE DIRECENCIAL
    userFechaNacimiento = models.DateField (auto_now=False, auto_now_add=False,null=True,blank=True)
    userEtnia =models.CharField (max_length=30)
    
    #ENFOQUE POBLACIONAL
    userCondicionDiscapacidad = models.CharField (max_length=60)
    
    #SOCIOECONOMICO
    userEstrato = models.CharField (max_length=3)
    
    #ESCOLARIDAD 
    userUltimoNivelEducativo = models.CharField (max_length=25)
    
    #ACCESO Y CONECTIVIDAD A MEDIOS TECNOLOGICOS
    userDispositivo = models.BooleanField (max_length=100,default=False)
                                         
    userTipoDispositivo = models.CharField (max_length=100,choices=TIPODISPOSITIVO)
    userConectividad = models.BooleanField (max_length=100,default=False)
    
    #SALUD
    userTipoAfiliacion = models.CharField (choices= AFILIACION ,max_length=100)
    userProfile =models.ImageField (upload_to='profile_pics', blank=True)

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
    
class Encuesta(models.Model):
    
    RESPUESTA = [
        ('0','Si'),
        ('1','No'),
    ]
     
    question = models.CharField(max_length=300)
    option = models.CharField(max_length=100)
    resultado = models.CharField(max_length=30, default='0', choices= RESPUESTA)
    
    def __str__(self):
        return self.question


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
    sonRespuesta = models.CharField (max_length=100)
    sonObservaciones = models.CharField (max_length=100)   
    encuesta = models.ManyToManyField(Encuesta)
    
    def __str__(self):
        return self.sonTitulo

    class Meta:
        db_table ='sondeo'
  
  


