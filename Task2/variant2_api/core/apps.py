from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.apps import apps

def create_default_position_handler(sender, **kwargs):
    Position = apps.get_model("core", "Position")
    Position.objects.get_or_create(name="Без должности")

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    def ready(self):
        post_migrate.connect(create_default_position_handler, sender=self)