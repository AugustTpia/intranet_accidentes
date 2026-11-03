# myapp/views.py

from django.shortcuts import render, redirect
from .models import Reporte
#from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Credenciales root 
# MarcoPavia
# paviafl0920
# MarcoPavia1
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
    return render(request, 'login.html')

def exit_login(request):
    return render (request, 'login.html')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def crear_reporte(request):
    if request.method == 'POST':
        reporte = Reporte(
            fecha=request.POST['fecha'],
            folio=request.POST['folio'],
            clave=request.POST['clave'],
            administrador=request.POST['administrador'],
            operador=request.POST['operador'],
            damage_vehiculo=request.POST['damage_vehiculo'],
            damage_bus=request.POST['damage_bus'],
            damage_others=request.POST['damage_others'],
            damage_others2=request.POST['damage_others2'],
            damage_others3=request.POST['damage_others3'],
            ubicacion=request.POST['ubicacion'],
            observaciones=request.POST['observaciones'],
            responsabilidad=request.POST['responsabilidad'],
            intervino=request.POST['intervino'],
            imagen1=request.FILES.get('imagen1'),
            imagen2=request.FILES.get('imagen2'),
            imagen3=request.FILES.get('imagen3'),
            imagen4=request.FILES.get('imagen4'),
            imagen5=request.FILES.get('imagen5'),
            imagen6=request.FILES.get('imagen6'),
        )
        reporte.save()
        return redirect('ver_reportes')
    return render(request, 'crear_reporte.html')

@login_required
def ver_reporte(request):
    reportes = Reporte.objects.all().order_by('-fecha_creacion')
    return render(request, 'ver_reporte.html', {'reportes': reportes})