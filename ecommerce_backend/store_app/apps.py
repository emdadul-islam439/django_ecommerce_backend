from django.apps import AppConfig


class StoreAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store_app'
    
    def ready(self):
        import store_app.signals