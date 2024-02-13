from django.apps import AppConfig


class ShopseeappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopseeapp'



    def ready(self):
        import shopseeapp.signals


    