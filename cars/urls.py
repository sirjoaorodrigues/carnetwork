# cars/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='cars/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/<str:username>/', views.perfil, name='perfil'),
    path('curtir/<int:post_id>/', views.curtir_post, name='curtir_post'),
    path('seguir/<str:username>/', views.seguir_usuario, name='seguir_usuario'),
    path('deixar-de-seguir/<str:username>/', views.deixar_de_seguir, name='deixar_de_seguir'),
]