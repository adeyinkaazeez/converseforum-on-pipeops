from django.apps import AppConfig


class SportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sports'
    def ready(self):
        import sports.signals

