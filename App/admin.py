from django.contrib import admin
from .models import *

# Register your models here

class MensajesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'message', 'file', 'created_at']
    search_fields = ['name']
    list_filter = ['estado']
    list_per_page: 10
    

    
admin.site.register(Mensajes, MensajesAdmin)
admin.site.register(Sondeo)
admin.site.register(Preguntas)