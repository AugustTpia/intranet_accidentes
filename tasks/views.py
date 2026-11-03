# myapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Reporte
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Lista
from .models import Administrador, Operador #Listas para formularios
from django.http import HttpResponse, JsonResponse
import csv
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from io import BytesIO
from django.db.models import Count, Q, Case, When, IntegerField, Window
from datetime import datetime
from django.db.models.functions import RowNumber
import json


# Credenciales root 
# MarcoPavia
# paviafl0920
# MarcoPavia1
"""
Funciones BETAAAA"""
@login_required(login_url='login')
def mapa(request):
    # ✅ Solo reportes con coordenadas, no los 17,000
    reportes = Reporte.objects.exclude(
        coordinates__isnull=True
    ).exclude(
        coordinates__exact=''
    ).order_by('-folio')
    
    reportes_data = []
    claves_unicas = set()
    rutas_unicas = set()
    
    for reporte in reportes:
        coordenadas = reporte.get_coordinates()
        
        # ✅ Construir URLs de imágenes solo si existen
        imagenes = []
        for i in range(1, 7):
            imagen_field = getattr(reporte, f'imagen{i}')
            if imagen_field:
                try:
                    imagenes.append(request.build_absolute_uri(imagen_field.url))
                except Exception:
                    pass
        
        claves_unicas.add(reporte.clave)
        rutas_unicas.add(reporte.ruta)
        
        reportes_data.append({
            'folio': reporte.folio,
            'fecha': str(reporte.fecha),  # ✅ str() evita errores de serialización
            'clave': reporte.clave,
            'operador': reporte.operador,
            'administrador': reporte.administrador,
            'ruta': reporte.ruta,
            'ubicacion': reporte.ubicacion,
            'damage_vehiculo': reporte.damage_vehiculo,
            'damage_bus': reporte.damage_bus,
            'damage_others': reporte.damage_others,
            'damage_others2': reporte.damage_others2,
            'damage_others3': reporte.damage_others3,
            'observaciones': reporte.observaciones,
            'intervino': reporte.intervino,
            'responsabilidad': reporte.responsabilidad,
            'costo_finiquito': float(reporte.costo_finiquito) if reporte.costo_finiquito else 0,
            'coordenadas': coordenadas,
            'imagenes': imagenes,
        })
    
    context = {
        'reportes': reportes,
        'reportes_json': json.dumps(reportes_data, ensure_ascii=False),  # ✅ para acentos
        'claves_unicas': sorted(claves_unicas),
        'rutas_unicas': sorted(rutas_unicas),
    }
    return render(request, 'ajustador/mapa.html', context)
@login_required(login_url='login_view')
def mapa_consulta(request):
    reportes = Reporte.objects.exclude(
        coordinates__isnull=True
    ).exclude(
        coordinates__exact=''
    ).order_by('-folio')
    
    reportes_data = []
    claves_unicas = set()
    rutas_unicas = set()
    
    for reporte in reportes:
        coordenadas = reporte.get_coordinates()
        
        imagenes = []
        for i in range(1, 7):
            imagen_field = getattr(reporte, f'imagen{i}')
            if imagen_field:
                try:
                    imagenes.append(request.build_absolute_uri(imagen_field.url))
                except Exception:  # ✅ Exception explícita, no bare except
                    pass
        
        claves_unicas.add(reporte.clave)
        rutas_unicas.add(reporte.ruta)
        
        reportes_data.append({
            'folio': reporte.folio,
            'fecha': str(reporte.fecha),  # ✅ str() para serialización segura
            'clave': reporte.clave,
            'operador': reporte.operador,
            'administrador': reporte.administrador,
            'ruta': reporte.ruta,
            'ubicacion': reporte.ubicacion,
            'damage_vehiculo': reporte.damage_vehiculo,
            'damage_bus': reporte.damage_bus,
            'damage_others': reporte.damage_others,
            'damage_others2': reporte.damage_others2,
            'damage_others3': reporte.damage_others3,
            'observaciones': reporte.observaciones,
            'intervino': reporte.intervino,
            'responsabilidad': reporte.responsabilidad,
            'costo_finiquito': float(reporte.costo_finiquito) if reporte.costo_finiquito else 0,
            'coordenadas': coordenadas,
            'imagenes': imagenes,
        })
    
    context = {
        'reportes': reportes,
        'reportes_json': json.dumps(reportes_data, ensure_ascii=False),  # ✅ acentos seguros
        'claves_unicas': sorted(claves_unicas),
        'rutas_unicas': sorted(rutas_unicas),
    }
    
    return render(request, 'consulta/mapa.html', context)
"""
Funciones que se reflejan en el usuario ajustador

"""
@login_required(login_url='login')
def home(request):
    return render(request, 'ajustador/home.html')

def editarReporte(request):
    reportes_list = Reporte.objects.all().order_by('-fecha')
    
    search_query = request.GET.get('search', '')
    if search_query:
        reportes_list = reportes_list.filter(
            Q(folio__icontains=search_query) | 
            Q(fecha__icontains=search_query) |
            Q(observaciones__icontains=search_query)
        )
    
    page_size = request.GET.get('page_size', 20)
    try:
        page_size = int(page_size)
    except ValueError:
        page_size = 20
    
    paginator = Paginator(reportes_list, page_size)
    page = request.GET.get('page', 1)
    
    try:
        reportes = paginator.page(page)
    except PageNotAnInteger:
        reportes = paginator.page(1)
    except EmptyPage:
        reportes = paginator.page(paginator.num_pages)
    
    context = {
        'reportes': reportes,
        'page_size': page_size,
        'search_query': search_query,
    }
    
    return render(request, 'ajustador/editarReporte.html', context)


def eliminar_reporte(request, reporte_id):
    """Vista para eliminar un reporte"""
    reporte = get_object_or_404(Reporte, id=reporte_id)
    
    if request.method == 'POST':
        if reporte.imagen1:
            reporte.imagen1.delete()
        if reporte.imagen2:
            reporte.imagen2.delete()
        if reporte.imagen3:
            reporte.imagen3.delete()
        if reporte.imagen4:
            reporte.imagen4.delete()
        if reporte.imagen5:
            reporte.imagen5.delete()
        if reporte.imagen6:
            reporte.imagen6.delete()
        
        folio = reporte.folio
        reporte.delete()
        messages.success(request, f'Reporte {folio} eliminado exitosamente.')
        return redirect('editarReporte')
    
    return redirect('editarReporte')


def editar_reporte_form(request, reporte_id):
    """Vista para mostrar y procesar el formulario de edición"""
    reporte = get_object_or_404(Reporte, id=reporte_id)
    
    if request.method == 'POST':
        reporte.titulo = request.POST.get('titulo', reporte.titulo)
        reporte.contenido = request.POST.get('contenido', reporte.contenido)
        reporte.fecha = request.POST.get('fecha', reporte.fecha)
        reporte.folio = request.POST.get('folio', reporte.folio)
        reporte.clave = request.POST.get('clave', reporte.clave)
        reporte.administrador = request.POST.get('administrador', reporte.administrador)
        reporte.ruta = request.POST.get('ruta', reporte.ruta)
        reporte.operador = request.POST.get('operador', reporte.operador)
        reporte.damage_vehiculo = request.POST.get('damage_vehiculo', reporte.damage_vehiculo)
        reporte.damage_bus = request.POST.get('damage_bus', reporte.damage_bus)
        reporte.damage_others = request.POST.get('damage_others', reporte.damage_others)
        reporte.damage_others2 = request.POST.get('damage_others2', reporte.damage_others2)
        reporte.damage_others3 = request.POST.get('damage_others3', reporte.damage_others3)
        reporte.ubicacion = request.POST.get('ubicacion', reporte.ubicacion)
        reporte.observaciones = request.POST.get('observaciones', reporte.observaciones)
        reporte.responsabilidad = request.POST.get('responsabilidad', reporte.responsabilidad)
        reporte.intervino = request.POST.get('intervino', reporte.intervino)
        
        costo_finiquito = request.POST.get('costo_finiquito', '')
        if costo_finiquito:
            try:
                reporte.costo_finiquito = float(costo_finiquito)
            except ValueError:
                reporte.costo_finiquito = None
        
        for i in range(1, 7):
            imagen_field = f'imagen{i}'
            if imagen_field in request.FILES:
                old_image = getattr(reporte, imagen_field)
                if old_image:
                    old_image.delete()
                setattr(reporte, imagen_field, request.FILES[imagen_field])
        
        reporte.save()
        messages.success(request, f'Reporte {reporte.folio} actualizado exitosamente.')
        return redirect('editarReporte')
    
    context = {
        'reporte': reporte,
    }
    
    return render(request, 'ajustador/editar_reporte_form.html', context)

@login_required(login_url='login')
def ver_reporte_main(request):
    reportes = Reporte.objects.all().order_by('-folio')

    for reporte in reportes:
        reporte.coordenadas_list = reporte.get_coordinates()
        reporte.tiene_coordenadas = reporte.has_coordinates()
        
        print(f"Reporte {reporte.folio}:")
        print(f"  - coordinates (raw): {reporte.coordinates}")
        print(f"  - coordenadas_list: {reporte.coordenadas_list}")
        print(f"  - tiene_coordenadas: {reporte.tiene_coordenadas}")
    
    context = {
        'reportes': reportes
    }
    return render(request, 'ajustador/ver_reportes.html', context)

@login_required(login_url='login_view')
def ver_reporte_consultor(request):
    reportes = Reporte.objects.all().order_by('-folio')

    for reporte in reportes:
        reporte.coordenadas_list = reporte.get_coordinates()
        reporte.tiene_coordenadas = reporte.has_coordinates()
        
        print(f"Reporte {reporte.folio}:")
        print(f"  - coordinates (raw): {reporte.coordinates}")
        print(f"  - coordenadas_list: {reporte.coordenadas_list}")
        print(f"  - tiene_coordenadas: {reporte.tiene_coordenadas}")
    
    context = {
        'reportes': reportes
    }
    return render(request, 'consulta/ver_reporte.html', context)


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  
            next_url = request.GET.get('next', 'home') 
            return redirect(next_url)
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'login/Ajustador.html')

@login_required(login_url='login')
def crear_reporte(request):
    if request.method == 'POST':
        try:
            # Debug: Imprimir datos recibidos
            print("=== DATOS RECIBIDOS ===")
            print("POST data:", request.POST)
            print("FILES data:", request.FILES)
            
            # Validar campos requeridos
            campos_requeridos = ['fecha', 'folio', 'clave', 'administrador', 'ruta', 
                                'operador', 'damage_vehiculo', 'damage_bus', 
                                'ubicacion', 'responsabilidad', 'intervino']
            
            campos_faltantes = []
            for campo in campos_requeridos:
                if not request.POST.get(campo):
                    campos_faltantes.append(campo)
            
            if campos_faltantes:
                messages.error(request, f'Faltan los siguientes campos: {", ".join(campos_faltantes)}')
                print(f"Campos faltantes: {campos_faltantes}")
                return render(request, 'ajustador/crear_reporte.html')
            
            # Obtener las coordenadas del formulario
            coordinates_json = request.POST.get('coordinates', '')
            
            # Crear el reporte
            reporte = Reporte(
                fecha=request.POST.get('fecha'),
                folio=request.POST.get('folio'),
                clave=request.POST.get('clave'),
                administrador=request.POST.get('administrador'),
                ruta=request.POST.get('ruta'),
                operador=request.POST.get('operador'),
                damage_vehiculo=request.POST.get('damage_vehiculo'),
                damage_bus=request.POST.get('damage_bus'),
                damage_others=request.POST.get('damage_others', ''),
                damage_others2=request.POST.get('damage_others2', ''),
                damage_others3=request.POST.get('damage_others3', ''),
                ubicacion=request.POST.get('ubicacion'),
                responsabilidad=request.POST.get('responsabilidad'),
                intervino=request.POST.get('intervino'),
            )
            
            # Manejar costo_finiquito (puede estar vacío)
            costo = request.POST.get('costo_finiquito', '').strip()
            if costo:
                try:
                    reporte.costo_finiquito = float(costo)
                except ValueError:
                    messages.error(request, 'El costo de finiquito debe ser un número válido')
                    return render(request, 'ajustador/crear_reporte.html')
            
            # Guardar observaciones
            reporte.observaciones = request.POST.get('observaciones', '')
            
            # Guardar coordenadas
            if coordinates_json and coordinates_json.strip():
                reporte.coordinates = coordinates_json
            
            # Guardar imágenes
            for i in range(1, 7):
                imagen = request.FILES.get(f'imagen{i}')
                if imagen:
                    setattr(reporte, f'imagen{i}', imagen)
            
            # Guardar el reporte
            reporte.save()
            
            print(f"✓ Reporte guardado exitosamente: {reporte.id}")
            messages.success(request, f'Reporte {reporte.folio} creado exitosamente!')
            return redirect('ver_reportes_main')
            
        except Exception as e:
            print(f"✗ ERROR al guardar: {str(e)}")
            print(f"Tipo de error: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            messages.error(request, f'Error al crear el reporte: {str(e)}')
            return render(request, 'ajustador/crear_reporte.html')
    
    # GET request
    return render(request, 'ajustador/crear_reporte.html')


#Modificar el ordenamiento según requerimientos /fecha/folio/ etccc

#Plantilla HTML de listas de Nombres = Administrador & Operador
def ver_listas(request):
    return render(request, 'mostrar_listas.html')
    #listas = Lista.objects.all()
    #return render(request, "mostrar.listas.html", {'listas': listas})
@login_required(login_url='login')
def tablas_de_posiciones_main(request):
    reportes = Reporte.objects.all()

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    responsabilidad_filter = request.GET.get('responsabilidad')
    operador_filter = request.GET.get('operador')

    #Filtros de Fecha primera tabla
    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
            reportes = reportes.filter(fecha__range=[fecha_inicio_dt, fecha_fin_dt])
        except ValueError:
            pass

    #Filtros
    if operador_filter:
        reportes = reportes.filter(operador__icontains=operador_filter)
    if responsabilidad_filter:
        reportes = reportes.filter(responsabilidad__icontains=responsabilidad_filter)

    # Accidentes Generales por Operador
    accidentes_generales = reportes.values('operador').annotate(
        numero_folios = Count('folio'),
        row_number=Window(
            expression=RowNumber(),
            order_by=Count('folio').desc()
        )).order_by('-numero_folios')
    
    #Unicos
    operadores_unicos = Reporte.objects.values_list('operador', flat=True).distinct()
    responsabilidades_unicas = Reporte.objects.values_list('responsabilidad', flat=True).distinct()

    detalles_operadores = {}

    for operador_data in accidentes_generales:
        operador = operador_data['operador']

        # Obtenemos todos los reportes de este operador (APLICANDO LOS MISMOS FILTROS)
        reportes_operador = Reporte.objects.filter(operador=operador)
        
        # Aplicar los mismos filtros que a la consulta principal
        if fecha_inicio and fecha_fin:
            try:
                fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
                reportes_operador = reportes_operador.filter(fecha__range=[fecha_inicio_dt, fecha_fin_dt])
            except ValueError:
                pass
        
        if responsabilidad_filter:
            reportes_operador = reportes_operador.filter(responsabilidad__icontains=responsabilidad_filter)

        detalles_operadores[operador] = {
            'reportes': list(reportes_operador.values('fecha', 'folio').order_by('-fecha')),
            'total_folios': operador_data['numero_folios'],
            'posicion': operador_data['row_number']
        }

    total_accidentes = Reporte.objects.count()

    context = {
        'total_accidentes': total_accidentes,
        'accidentes_generales': accidentes_generales,
        'detalles_operadores': detalles_operadores,
        'operadores_unicos': operadores_unicos,
        'responsabilidades_unicas': responsabilidades_unicas,
        'filtros': {
            'fecha_inicio': fecha_inicio or '',
            'fecha_fin': fecha_fin or '',
            'operador': operador_filter or '',
            'responsabilidad': responsabilidad_filter or '',
        }
    }

    return render(request, 'ajustador/Top_list.html', context)


@login_required(login_url='login')
def reporte_estadisticas_main(request):
    # Obtener todos los registros inicialmente
    reportes = Reporte.objects.all()
    
    # Obtener parámetros de filtro
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    ruta_filter = request.GET.get('ruta')
    folio_filter = request.GET.get('folio')
    clave_filter = request.GET.get('clave')
    administrador_filter = request.GET.get('administrador')
    operador_filter = request.GET.get('operador')
    responsabilidad_filter = request.GET.get('responsabilidad')
    intervino_filter = request.GET.get('intervino')
    export_format = request.GET.get('export')
    
    # Aplicar filtros
    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
            reportes = reportes.filter(fecha__range=[fecha_inicio_dt, fecha_fin_dt])
        except ValueError:
            pass
    
    if ruta_filter:
        reportes = reportes.filter(ruta__icontains=ruta_filter)
    if folio_filter:
        reportes = reportes.filter(folio__icontains=folio_filter)
    if clave_filter:
        reportes = reportes.filter(clave__icontains=clave_filter)
    if administrador_filter:
        reportes = reportes.filter(administrador__icontains=administrador_filter)
    if operador_filter:
        reportes = reportes.filter(operador__icontains=operador_filter)
    if responsabilidad_filter:
        reportes = reportes.filter(responsabilidad__icontains=responsabilidad_filter)
    if intervino_filter:
        reportes =  reportes.filter(intervino__icontains=intervino_filter)

    # Obtener total general
    # Suma total de registros con filtros
    total_general = reportes.count()
    qualitas_general = reportes.count()

    
    # Agrupar por ruta y contar
    estadisticas_rutas = reportes.values('ruta').annotate(total=Count('id')).order_by('-total')

    # Información para Sección Responsabilidad e Intervenciones
    total_con_responsabilidad = reportes.filter(responsabilidad="Si").count()

    total_sin_responsabilidad = reportes.filter(responsabilidad="No").count()

    participacion_qualitas_con = reportes.filter(
        responsabilidad="Si", 
        intervino="Si Intervino"
    ).count()

    # Participación Qualitas SIN responsabilidad
    participacion_qualitas_sin = reportes.filter(
        responsabilidad="No", 
        intervino="Si Intervino"
    ).count()

    participacion_general = participacion_qualitas_con + participacion_qualitas_sin

    # Agrupar por ruta y contar responsabilidades "Si" y "No"  
    estadisticas_qualitas = reportes.values('ruta').annotate(
    total_si=Count(Case(
        When(responsabilidad="Si", then=1),
        output_field=IntegerField()
    )),
    total_no=Count(Case(
        When(responsabilidad="No", then=1), 
        output_field=IntegerField()
    )),
    intervino_si=Count(Case(
        When(intervino="Si Intervino", then=1),
        output_field=IntegerField()
    )),
    intervino_no=Count(Case(
        When(intervino="No intervino", then=1), 
        output_field=IntegerField()
    )),
    totales=Count('id')).order_by('-ruta')
    
    # Obtener lista de rutas únicas para el dropdown
    rutas_unicas = Reporte.objects.values_list('ruta', flat=True).distinct()

    #Obtener lista de responsabilidades únicas para el dropdown
    responsabilidades_unicas = Reporte.objects.values_list('responsabilidad', flat=True).distinct()

    #Obtener lista de administradores únicos para el dropdown
    administradores_unicos = Reporte.objects.values_list('administrador', flat=True).distinct()

    #Obtener lista de claves únicas
    clave_unica = Reporte.objects.values_list('clave', flat=True).distinct()

    #Obtener lista de qualitas participa o no
    qualitas_unico = Reporte.objects.values_list('intervino', flat=True).distinct()
    
    # Exportar datos si se solicita
    if export_format:
        return exportar_datos(reportes, export_format)
    
    context = {
        'estadisticas_rutas': estadisticas_rutas,
        'total_con_responsabilidad': total_con_responsabilidad,
        'total_sin_responsabilidad': total_sin_responsabilidad,
        'participacion_qualitas_con': participacion_qualitas_con,
        'participacion_qualitas_sin': participacion_qualitas_sin,
        'participacion_general': participacion_general,
        'estadisticas_qualitas': estadisticas_qualitas,
        'total_general': total_general,
        'qualitas_general': qualitas_general,
        'reportes_filtrados': reportes,
        'rutas_unicas': rutas_unicas,
        'responsabilidades_unicas': responsabilidades_unicas,
        'administradores_unicos': administradores_unicos,
        'clave_unica': clave_unica,
        'qualitas_unico': qualitas_unico,
        'filtros': {
            'fecha_inicio': fecha_inicio or '',
            'fecha_fin': fecha_fin or '',
            'ruta': ruta_filter or '',
            'folio': folio_filter or '',
            'clave': clave_filter or '',
            'administrador': administrador_filter or '',
            'operador': operador_filter or '',
            'responsabilidad': responsabilidad_filter or '',
            'intervino': intervino_filter or '',
        }
    }
    
    return render(request, 'ajustador/estadisticas_reporte.html', context)

def mostrar_listas(request):
    return render(request, 'ajustador/mostrar_listas.html')

def vista_prueba_ajustador(request):
    return render(request, 'ajustador/prueba.html')


#Modelo de estructura de formulario, para agregar un Administrador
def agregar_Administrador(request):
    if request.method == 'POST':
        lista_Admin = Administrador(
            nombre_Admin=request.POST['nombre_Admin'],
            alias_Admin=request.POST['alias_Admin'],
            comentario_Admin=request.POST['comentario_Admin'],
        )
        lista_Admin.save()
        return redirect('home')
    return render (request, 'ajustador/Administrador_formulario.html')

#Falta implementar HTML y path de URL para guardar un operador
def agregar_Operador(request):
    if request.method== 'POST':
        lista_Oper = Operador(
            nombre_Operador=request.POST['nombre_Operador'],
            alias_Operador=request.POST['alias_Operador'],
            comentario_Operador=request.POST['comentario_Operador'],

        )



""" 
Funciones que se reflejan en los usuarios CONSULTORES

"""


def viewer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            next_url = request.GET.get('next', 'home_view')
            return redirect(next_url)
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    return render(request, 'login/Consultor.html')

@login_required(login_url='login_view')
def home_view(request):
    return render(request, 'consulta/home.html')

#Tabla de Posiciones de Accidentes
@login_required(login_url='login_view')
def tablas_de_posiciones(request):
    reportes = Reporte.objects.all()

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    responsabilidad_filter = request.GET.get('responsabilidad')
    operador_filter = request.GET.get('operador')

    #Filtros de Fecha primera tabla
    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
            reportes = reportes.filter(fecha__range=[fecha_inicio_dt, fecha_fin_dt])
        except ValueError:
            pass

    #Filtros
    if operador_filter:
        reportes = reportes.filter(operador__icontains=operador_filter)
    if responsabilidad_filter:
        reportes = reportes.filter(responsabilidad__icontains=responsabilidad_filter)

    # Accidentes Generales por Operador
    accidentes_generales = reportes.values('operador').annotate(
        numero_folios = Count('folio'),
        row_number=Window(
            expression=RowNumber(),
            order_by=Count('folio').desc()
        )).order_by('-numero_folios')
    
    #Unicos
    operadores_unicos = Reporte.objects.values_list('operador', flat=True).distinct()
    responsabilidades_unicas = Reporte.objects.values_list('responsabilidad', flat=True).distinct()

    detalles_operadores = {}

    for operador_data in accidentes_generales:
        operador = operador_data['operador']

        # Obtenemos todos los reportes de este operador (APLICANDO LOS MISMOS FILTROS)
        reportes_operador = Reporte.objects.filter(operador=operador)
        
        # Aplicar los mismos filtros que a la consulta principal
        if fecha_inicio and fecha_fin:
            try:
                fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
                fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
                reportes_operador = reportes_operador.filter(fecha__range=[fecha_inicio_dt, fecha_fin_dt])
            except ValueError:
                pass
        
        if responsabilidad_filter:
            reportes_operador = reportes_operador.filter(responsabilidad__icontains=responsabilidad_filter)

        detalles_operadores[operador] = {
            'reportes': list(reportes_operador.values('fecha', 'folio').order_by('-fecha')),
            'total_folios': operador_data['numero_folios'],
            'posicion': operador_data['row_number']
        }

    total_accidentes = Reporte.objects.count()

    context = {
        'total_accidentes': total_accidentes,
        'accidentes_generales': accidentes_generales,
        'detalles_operadores': detalles_operadores,
        'operadores_unicos': operadores_unicos,
        'responsabilidades_unicas': responsabilidades_unicas,
        'filtros': {
            'fecha_inicio': fecha_inicio or '',
            'fecha_fin': fecha_fin or '',
            'operador': operador_filter or '',
            'responsabilidad': responsabilidad_filter or '',
        }
    }

    return render(request, 'consulta/top_list.html', context)
@login_required(login_url='login_view')
def reporte_estadisticas(request):
    # Obtener todos los registros inicialmente
    reportes = Reporte.objects.all()
    
    # Obtener parámetros de filtro
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    ruta_filter = request.GET.get('ruta')
    folio_filter = request.GET.get('folio')
    clave_filter = request.GET.get('clave')
    administrador_filter = request.GET.get('administrador')
    operador_filter = request.GET.get('operador')
    responsabilidad_filter = request.GET.get('responsabilidad')
    intervino_filter = request.GET.get('intervino')
    export_format = request.GET.get('export')
    
    # Aplicar filtros
    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
            reportes = reportes.filter(fecha__range=[fecha_inicio_dt, fecha_fin_dt])
        except ValueError:
            pass
    
    if ruta_filter:
        reportes = reportes.filter(ruta__icontains=ruta_filter)
    if folio_filter:
        reportes = reportes.filter(folio__icontains=folio_filter)
    if clave_filter:
        reportes = reportes.filter(clave__icontains=clave_filter)
    if administrador_filter:
        reportes = reportes.filter(administrador__icontains=administrador_filter)
    if operador_filter:
        reportes = reportes.filter(operador__icontains=operador_filter)
    if responsabilidad_filter:
        reportes = reportes.filter(responsabilidad__icontains=responsabilidad_filter)
    if intervino_filter:
        reportes =  reportes.filter(intervino__icontains=intervino_filter)

    # Obtener total general
    # Suma total de registros con filtros
    total_general = reportes.count()
    qualitas_general = reportes.count()

    
    # Agrupar por ruta y contar
    estadisticas_rutas = reportes.values('ruta').annotate(total=Count('id')).order_by('-total')

    # Información para Sección Responsabilidad e Intervenciones
    total_con_responsabilidad = reportes.filter(responsabilidad="Si").count()

    total_sin_responsabilidad = reportes.filter(responsabilidad="No").count()

    participacion_qualitas_con = reportes.filter(
        responsabilidad="Si", 
        intervino="Si Intervino"
    ).count()

    # Participación Qualitas SIN responsabilidad
    participacion_qualitas_sin = reportes.filter(
        responsabilidad="No", 
        intervino="Si Intervino"
    ).count()

    participacion_general = participacion_qualitas_con + participacion_qualitas_sin

    # Agrupar por ruta y contar responsabilidades "Si" y "No"  
    estadisticas_qualitas = reportes.values('ruta').annotate(
    total_si=Count(Case(
        When(responsabilidad="Si", then=1),
        output_field=IntegerField()
    )),
    total_no=Count(Case(
        When(responsabilidad="No", then=1), 
        output_field=IntegerField()
    )),
    intervino_si=Count(Case(
        When(intervino="Si Intervino", then=1),
        output_field=IntegerField()
    )),
    intervino_no=Count(Case(
        When(intervino="No intervino", then=1), 
        output_field=IntegerField()
    )),
    totales=Count('id')).order_by('-ruta')
    
    # Obtener lista de rutas únicas para el dropdown
    rutas_unicas = Reporte.objects.values_list('ruta', flat=True).distinct()

    #Obtener lista de responsabilidades únicas para el dropdown
    responsabilidades_unicas = Reporte.objects.values_list('responsabilidad', flat=True).distinct()

    #Obtener lista de administradores únicos para el dropdown
    administradores_unicos = Reporte.objects.values_list('administrador', flat=True).distinct()

    #Obtener lista de claves únicas
    clave_unica = Reporte.objects.values_list('clave', flat=True).distinct()

    #Obtener lista de qualitas participa o no
    qualitas_unico = Reporte.objects.values_list('intervino', flat=True).distinct()
    
    # Exportar datos si se solicita
    if export_format:
        return exportar_datos(reportes, export_format)
    
    context = {
        'estadisticas_rutas': estadisticas_rutas,
        'total_con_responsabilidad': total_con_responsabilidad,
        'total_sin_responsabilidad': total_sin_responsabilidad,
        'participacion_qualitas_con': participacion_qualitas_con,
        'participacion_qualitas_sin': participacion_qualitas_sin,
        'participacion_general': participacion_general,
        'estadisticas_qualitas': estadisticas_qualitas,
        'total_general': total_general,
        'qualitas_general': qualitas_general,
        'reportes_filtrados': reportes,
        'rutas_unicas': rutas_unicas,
        'responsabilidades_unicas': responsabilidades_unicas,
        'administradores_unicos': administradores_unicos,
        'clave_unica': clave_unica,
        'qualitas_unico': qualitas_unico,
        'filtros': {
            'fecha_inicio': fecha_inicio or '',
            'fecha_fin': fecha_fin or '',
            'ruta': ruta_filter or '',
            'folio': folio_filter or '',
            'clave': clave_filter or '',
            'administrador': administrador_filter or '',
            'operador': operador_filter or '',
            'responsabilidad': responsabilidad_filter or '',
            'intervino': intervino_filter or '',
        }
    }
    
    return render(request, 'consulta/estadisticas_reporte.html', context)

"""
Funciones para exportar datos
"""

def exportar_datos(reportes, format):
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reportes_filtrados.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Folio', 'Fecha', 'Ruta', 'Clave', 'Administrador', 
            'Operador', 'Ubicación', 'Responsabilidad', 'Intervino', 'money'
        ])
        
        for reporte in reportes:
            writer.writerow([
                reporte.folio, reporte.fecha, reporte.ruta, reporte.clave,
                reporte.administrador, reporte.operador, reporte.ubicacion,
                reporte.responsabilidad, reporte.intervino, reporte.costo_finiquito
            ])
        
        return response
    
    elif format == 'excel':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="reportes_filtrados.xlsx"'
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Reportes"
        
        # Encabezados
        ws.append([
            'Folio', 'Fecha', 'Ruta', 'Clave', 'Administrador', 
            'Operador', 'Ubicación', 'Responsabilidad', 'Intervino', '$ Costo Finiquito'
        ])
        
        # Datos
        for reporte in reportes:
            ws.append([
                reporte.folio, reporte.fecha, reporte.ruta, reporte.clave,
                reporte.administrador, reporte.operador, reporte.ubicacion,
                reporte.responsabilidad, reporte.intervino, reporte.costo_finiquito
            ])
        
        output = BytesIO()
        wb.save(output)
        response.write(output.getvalue())
        
        return response
    
    return JsonResponse({'error': 'Formato no soportado'}, status=400)




