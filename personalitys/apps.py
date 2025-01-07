from django.apps import AppConfig


class PersonalitysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'personalitys'
    def ready(self):
        import personalitys.signals
