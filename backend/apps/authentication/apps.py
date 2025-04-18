from django.apps import AppConfig

# Activate authetntication signals
def ready(self):
    import apps.authentication.signals


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
