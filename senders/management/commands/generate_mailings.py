import random
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand

from senders.models import Mailing, Message, Recipient
from users.models import CustomUser


class Command(BaseCommand):
    help = "Генерация случайных рассылок"

    def handle(self, *args, **kwargs):
        number_of_mailings = 30

        for _ in range(number_of_mailings):
            start_date = datetime.now()
            user = CustomUser.objects.order_by("?").first()
            message = Message.objects.filter(owner=user).order_by("?").first()
            if not message:
                self.stdout.write(
                    self.style.WARNING(
                        "Пропуск создания рассылки: "
                        f"у пользователя {user.username} нет сообщений"
                    )
                )
                continue

            mailing = Mailing.objects.create(
                start_date=start_date,
                end_date=start_date + timedelta(days=random.randint(1, 7)),
                status=random.choice(["created", "started", "finished"]),
                message=message,
                owner=user,
            )

            recipients = Recipient.objects.filter(owner=user).order_by("?")[
                : random.randint(1, 10)
            ]
            mailing.recipients.set(recipients)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Рассылка с темой '{mailing.message.subject}' "
                    f"создана для пользователя {user.username}"
                )
            )
