"""
URL configuration for form_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from tasks import views

urlpatterns = [

    
    #URLS de Ajustador
    #path('admin/', admin.site.urls), #URL del Panel de Administración
    path('ajustador/', views.home, name = 'home' ),
    path('login/', views.user_login, name = 'login'),
    path('crear_reporte/', views.crear_reporte, name = 'crear_reporte'),
    path('editarReporte/', views.editarReporte, name = 'editarReporte'),
    path('editarReporte/editar/<int:reporte_id>/', views.editar_reporte_form, name='editar_reporte_form'),
    path('editarReporte/eliminar/<int:reporte_id>/', views.eliminar_reporte, name='eliminar_reporte'),
    path('ver_reportes_main/', views.ver_reporte_main, name = 'ver_reportes_main'),
    path('reporte_estadisticas_main/', views.reporte_estadisticas_main, name = 'reporte_estadisticas_main'),
    path('top_listss/', views.tablas_de_posiciones_main, name = 'top_listss'),
    path('mostrar_listas/', views.mostrar_listas, name = 'mostrar_listas'),
    path('formulario_administrador/', views.agregar_Administrador, name = "formulario_administrador"),
    
    path('vista_prueba_ajustador/', views.vista_prueba_ajustador, name='vista_prueba_ajustador'),


    #URLS de Consultor
    path('login_view/', views.viewer_login, name = 'login_view'),
    path('consultor/', views.home_view, name = 'home_view'),
    path('exit_login/', views.user_login, name = 'exit_login'),
    path('ver_reportes/', views.ver_reporte_consultor, name = 'ver_reportes'),
    path('reporte_estadisticas/', views.reporte_estadisticas, name = 'reporte_estadisticas'),
    path('top_lists/', views.tablas_de_posiciones, name='top_lists'),
    path('ver_listas/', views.ver_listas, name= 'ver_listas'),

    #Funciones MAP
    path('mapa/', views.mapa, name='mapa'),
    path('mapa_general/', views.mapa_consulta, name='mapa_general'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
