from django.apps import AppConfig


class MajaslapaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'majaslapa'


class UsersConfig(AppConfig):
    name = 'majaslapa'

    def ready(self):
        import majaslapa.signals