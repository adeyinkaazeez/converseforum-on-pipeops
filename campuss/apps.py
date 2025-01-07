from django.apps import AppConfig


class CampussConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'campuss'

    def ready(self):
        import campuss.signals
