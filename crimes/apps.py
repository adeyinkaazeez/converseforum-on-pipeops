from django.apps import AppConfig


class CrimesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'crimes'

    def ready(self):
        import crimes.signals
