from django.apps import AppConfig


class MenuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'menu' 

    def ready(self) -> None:
        from menu import signals

        return super().ready()
