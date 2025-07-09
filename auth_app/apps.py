# grant_app/apps.py

from django.apps import AppConfig

class AuthAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auth_app' # Ilovangizning haqiqiy nomi

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        import auth_app.signals # Signallar faylini import qilish