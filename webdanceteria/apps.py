from django.apps import AppConfig

class WebdanceteriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webdanceteria'

    def ready(self):
        import webdanceteria.signals
