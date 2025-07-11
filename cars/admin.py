# cars/admin.py

from django.contrib import admin
from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'cidade', 'criado_em']
    search_fields = ['user__username', 'cidade']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['autor', 'criado_em', 'total_curtidas']
    list_filter = ['criado_em']
    search_fields = ['autor__username', 'conteudo']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['autor', 'post', 'criado_em']
    list_filter = ['criado_em']
    search_fields = ['autor__username', 'conteudo']

@admin.register(Seguidor)
class SeguidorAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'seguindo', 'criado_em']
    search_fields = ['usuario__username', 'seguindo__username']