# Guía de Despliegue en Servidor Nuevo (vía USB)

Para mover este sistema a otra máquina usando una memoria USB, sigue estos pasos:

## 1. Archivos que debes llevar en la USB
Copia toda la carpeta del proyecto a tu memoria USB. Asegúrate de que incluya:
- Carpeta `media/`: Contiene todas las imágenes.
- Carpeta `nginx/`: Configuración del servidor web.
- Archivo `.env`: Contiene las contraseñas y claves.
- Archivo `docker-compose.yml` y `Dockerfile`.
- **Archivo `database_backup.sql`**: (Generado automáticamente para esta migración).

## 2. Requisitos en la máquina de destino
- **Docker** instalado.
- **Docker Compose** instalado.

## 3. Pasos para el primer despliegue
Una vez copies la carpeta en la nueva máquina, abre una terminal en esa ubicación y ejecuta:

### A. Levantar el sistema
```bash
docker-compose up -d --build
```

### B. Restaurar la base de datos
Dado que es una base de datos nueva, debemos cargar el respaldo:
```bash
# Espera unos 10 segundos a que MySQL inicie, luego ejecuta:
docker exec -i devel_ajustador_django-db-1 mysql -udjango_user -pdjango_pass ajustador_db < database_backup.sql
```

## Notas Adicionales:
- El sistema está configurado para ejecutarse en el puerto **80**. Si el servidor nuevo tiene ocupado ese puerto, cámbialo en el `docker-compose.yml` bajo la sección de `nginx`.
- Las imágenes en `media/` ya están sincronizadas y se cargarán automáticamente.
- He corregido los errores de advertencia en el archivo `docker-compose.yml` para que el despliegue sea limpio.
