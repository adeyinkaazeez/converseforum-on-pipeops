from django.apps import AppConfig


class SportArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sport_articles'
    def ready(self):
        import sport_articles.signals
