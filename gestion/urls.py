from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    # === RUTAS PÚBLICAS (para visitantes) ===
    path('', views.home_public, name='home_public'),
    path('petroglifo/<int:simbolo_id>/', views.publico_detalle, name='publico_detalle'),
    
    # === RUTAS PRIVADAS (requieren login) ===
    path('mis-investigaciones/', views.catalogo_mis_investigaciones, name='mis_investigaciones'),
    path('catalogo/', views.catalogo_todas_investigaciones, name='catalogo_todas'),
    #el resto igual
    path('', views.catalogo_mis_investigaciones, name='mis_investigaciones'),
    path('catalogo/', views.catalogo_todas_investigaciones, name='catalogo_todas'),
    path('simbolo/<int:simbolo_id>/', views.simbolo_detalle, name='simbolo_detalle'),
    path('simbolo/nuevo/', views.crear_simbolo, name='crear_simbolo'),
    path('simbolo/<int:simbolo_id>/editar/', views.editar_simbolo, name='editar_simbolo'),
    path('investigadores/nuevo/', views.crear_investigador, name='crear_investigador'),
    path('rutas/', views.rutas_servidor, name='rutas_servidor'),
]
