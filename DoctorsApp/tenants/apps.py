from django.apps import AppConfig


class MainappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DoctorsApp.tenants'

    def ready(self):
        import DoctorsApp.tenants.signals

