from django.apps import AppConfig


class BusinessArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'business__articles'

    def ready(self):
        import business__articles.signals
