from django.apps import AppConfig


class BackgroundTaskAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'background_task_app'
    
    def ready(self):
        import background_task_app.signals