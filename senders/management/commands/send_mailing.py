from django.core.management.base import BaseCommand

from senders.models import Mailing
from senders.tasks import send_mailing


class Command(BaseCommand):
    help = "Отправка рассылок через командную строку"

    def add_arguments(self, parser):
        parser.add_argument(
            "--mailing_id",
            type=int,
            help="ID рассылки для отправки (опционально)",
        )

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]
        if mailing_id:
            try:
                mailing = Mailing.objects.get(pk=mailing_id)
                send_mailing(mailing)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Рассылка с ID {mailing_id} отправлена"
                    )
                )
            except Mailing.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR("Указанная рассылка не найдена")
                )
        else:
            send_mailing()
            self.stdout.write(
                self.style.SUCCESS("Все активные рассылки отправлены")
            )
