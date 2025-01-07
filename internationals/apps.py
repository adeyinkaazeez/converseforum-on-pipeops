from django.apps import AppConfig


class InternationalsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'internationals'

    def ready(self):
        import internationals.signals
