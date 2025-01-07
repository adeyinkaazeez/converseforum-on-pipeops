from django.apps import AppConfig


class PoliticalArticlesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'political_articles'

    def ready(self):
        import political_articles.signals
