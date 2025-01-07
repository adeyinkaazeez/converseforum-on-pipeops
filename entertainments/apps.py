from django.apps import AppConfig


class EntertainmentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'entertainments'

    def ready(self):
        import entertainments.signals
