from django.apps import AppConfig


class ReligionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'religions'
    def ready(self):
        import religions.signals
