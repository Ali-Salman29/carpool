from django.apps import AppConfig


class UploadConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rides'

    def ready(self):
        from . import signals  # pylint: disable=unused-import
