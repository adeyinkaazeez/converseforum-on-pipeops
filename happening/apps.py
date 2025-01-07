from django.apps import AppConfig


class HappeningConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'happening'

    def ready(self):
        import happening.signals
