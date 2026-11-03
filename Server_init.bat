@echo off
title 🚀 Waitress (Django Backend) - Reinicio Automático
cd C:\Users\marco\Desktop\VSC\devel_ajustador_Django

:inicio
echo.
echo ========================================
echo [%date% %time%] INICIANDO WAITRESS
echo ========================================
echo.

call venv\Scripts\Activate.bat

waitress-serve --listen=127.0.0.1:8000 --threads=8 --channel-timeout=60 form_web.wsgi:application

echo.
echo ========================================
echo [%date% %time%] SERVICIO DETENIDO
echo Reiniciando en 10 segundos...
echo ========================================
echo.

echo %date% %time% - Reinicio automatico >> historial_reinicios.log
timeout /t 10 /nobreak
goto inicio