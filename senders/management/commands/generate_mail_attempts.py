import random

from django.core.management.base import BaseCommand

from senders.models import MailAttemptToSend, Mailing
from users.models import CustomUser


class Command(BaseCommand):
    help = "Генерация случайных попыток рассылок"

    def handle(self, *args, **kwargs):
        number_of_attempts = 50

        i: int = 0
        while i < number_of_attempts:
            mailing = (
                Mailing.objects.filter(
                    owner=CustomUser.objects.order_by("?").first()
                )
                .order_by("?")
                .first()
            )

            if not mailing:
                self.stdout.write(
                    self.style.ERROR("У пользователя нет доступных рассылок"),
                )
                continue
            status = random.choice(["success", "failure"])
            attempt = MailAttemptToSend.objects.create(
                mailing=mailing,
                status=status,
                server_response=(
                    "Успешно" if status == "success" else "Ошибка при отправке"
                ),
            )

            i += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f"Попытка рассылки для {attempt.mailing.message.subject} "
                    f'с результатом "{status}" создана'
                )
            )
