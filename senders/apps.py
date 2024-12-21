from django.apps import AppConfig


class SendersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "senders"
    verbose_name = "Рассылки"

    # def ready(self):
    #     from senders.tasks import start_scheduler
    #
    #     start_scheduler()
