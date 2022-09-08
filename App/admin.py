from django.contrib import admin
from .models import *
# from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin

# Register your models here

class usuarioPerzonalidado(UserAdmin):
    fieldsets = ()
    add_fieldsets = (
        (None, {
            'fields': ('username','email','password1','password2','userDocumento'
                ,'userNombreCompleto','userApellidos','userSexo','is_active',
                'userTelefono','userTelefonoFijo','userCorreo','userMunicipio','userDireccion',
                'userBarrio','userFechaNacimiento','userEtnia','userCondicionDiscapacidad','userEstrato',
                'userUltimoNivelEducativo','userDispositivo','userTipoDispositivo','userConectividad',
                'userTipoAfiliacion')
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'userProfile')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',) 

class MensajesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'message', 'file', 'created_at']
    search_fields = ['name']
    list_filter = ['estado']
    list_per_page: 10
    

admin.site.register(UsuarioPerzonalizado,usuarioPerzonalidado)     
admin.site.register(Mensajes, MensajesAdmin)
admin.site.register(Sondeo)
admin.site.register(Encuesta)