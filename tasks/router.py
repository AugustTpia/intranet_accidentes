class AuthRouter:
    """
    Un router para controlar todas las operaciones de base de datos en los modelos de autenticación.
    """
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'auth' or model._meta.app_label == 'admin':
            return 'default'  # Usar SQLite para autenticación
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'auth' or model._meta.app_label == 'admin':
            return 'default'  # Usar SQLite para autenticación
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'auth' or obj2._meta.app_label == 'auth':
            return True  # Permitir relaciones para modelos de autenticación
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'auth' or app_label == 'admin':
            return db == 'default'  # Migrar solo a SQLite para autenticación
        return None