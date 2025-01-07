from django.apps import AppConfig


class CelebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'celeb'
    def ready(self):
        import celeb.signals
