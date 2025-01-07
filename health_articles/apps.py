from django.apps import AppConfig


class HealthArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'health_articles'

    def ready(self):
        import health_articles.signals
