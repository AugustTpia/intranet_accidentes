# Guía de Migración a Docker y MySQL

Se han generado los archivos necesarios para dockerizar la aplicación Django y migrar la base de datos a MySQL.

## Archivos Creados/Modificados:

1.  **`Dockerfile`**: Define la imagen de la aplicación (Python 3.11-slim, instala dependencias de MySQL).
2.  **`docker-compose.yml`**: Orquesta tres servicios:
    *   `db`: Base de datos MySQL 8.0.
    *   `web`: Aplicación Django (Gunicorn).
    *   `nginx`: Proxy inverso para servir estáticos y redirigir tráfico.
3.  **`nginx/nginx.conf`**: Configuración de Nginx para el proxy y archivos estáticos.
4.  **`entrypoint.sh`**: Script que espera a la DB, corre migraciones y arranca el servidor.
5.  **`.env`**: Variables de entorno para credenciales y configuración.
6.  **`form_web/settings.py`**: Actualizado para usar MySQL y variables de entorno.
7.  **`requirements.txt`**: Actualizado con drivers de MySQL y convertido a UTF-8.

## Instrucciones de Despliegue

### 1. Preparar la migración de datos
Desde tu terminal actual (con el entorno virtual activo), exporta los datos actuales:
```powershell
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data.json
```

### 2. Construir y levantar contenedores
En la raíz del proyecto:
```powershell
docker-compose up -d --build
```

### 3. Cargar los datos en el nuevo MySQL
```powershell
docker-compose exec web python manage.py loaddata data.json
```

## Correcciones Realizadas:

*   **Seguridad**: Se movieron las credenciales a un archivo `.env`.
*   **Portabilidad**: Se corrigió la codificación de `requirements.txt` (UTF-16 a UTF-8) para compatibilidad con Linux.
*   **Eficiencia**: Nginx ahora maneja los archivos estáticos (`/static/`) y media (`/media/`) directamente.
*   **Robustez**: Se añadió un script `entrypoint.sh` que asegura que la base de datos esté lista antes de que Django intente conectar.
