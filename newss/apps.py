from django.apps import AppConfig


class NewssConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newss'
    def ready(self):
        import newss.signals
