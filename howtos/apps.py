from django.apps import AppConfig


class HowtosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'howtos'

    def ready(self):
        import howtos.signals
