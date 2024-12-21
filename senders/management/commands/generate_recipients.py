from django.core.management.base import BaseCommand
from faker import Faker

from senders.models import Recipient
from users.models import CustomUser

fake = Faker()


class Command(BaseCommand):
    help = "Генерация случайных получателей для рассылок"

    def handle(self, *args, **kwargs):
        number_of_recipients = 50

        for _ in range(number_of_recipients):
            user = CustomUser.objects.order_by("?").first()
            recipient = Recipient.objects.create(
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                middle_name=fake.last_name(),
                comment=fake.text(),
                owner=user,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Получатель {recipient.first_name} {recipient.last_name} "
                    f"создан для пользователя {user.username}"
                )
            )
