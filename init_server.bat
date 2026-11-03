@echo off
title 🚀 Servidor Django - Reinicio Automático
cd C:\Users\marco\Desktop\VSC\devel_ajustador_Django

:inicio
echo.
echo ========================================
echo [%date% %time%] INICIANDO SERVIDOR DJANGO
echo ========================================
echo.

:: Activar entorno virtual
call venv\Scripts\Activate.bat

:: Ejecutar Waitress con configuración optimizada
waitress-serve --listen=0.0.0.0:80 --threads=8 --channel-timeout=60 form_web.wsgi:application

:: Si llegamos aquí, el servidor se detuvo
echo.
echo ========================================
echo [%date% %time%] SERVICIO DETENIDO
echo Reiniciando en 10 segundos...
echo ========================================
echo.

:: Registrar el reinicio
echo %date% %time% - Reinicio automatico >> historial_reinicios.log

timeout /t 10 /nobreak
goto inicio