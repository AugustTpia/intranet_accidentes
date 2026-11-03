#!/bin/bash

# Esperar a que la base de datos esté lista
echo "Esperando a la base de datos..."
while ! nc -z $DB_HOST $DB_PORT; do
  sleep 0.1
done
echo "Base de datos lista."

# Realizar migraciones
echo "Realizando migraciones..."
python manage.py migrate

# Recolectar archivos estáticos
echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

# Iniciar Gunicorn
echo "Iniciando Gunicorn..."
exec gunicorn form_web.wsgi:application --bind 0.0.0.0:8000 --workers 3
