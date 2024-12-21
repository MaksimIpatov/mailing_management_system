from django.core.management.base import BaseCommand
from faker import Faker

from senders.models import Message
from users.models import CustomUser

fake = Faker()


class Command(BaseCommand):
    help = "Генерация случайных сообщений для рассылок"

    def handle(self, *args, **kwargs):
        number_of_messages = 10

        for _ in range(number_of_messages):
            user = CustomUser.objects.order_by("?").first()
            message = Message.objects.create(
                subject=fake.sentence(nb_words=6),
                body=fake.text(max_nb_chars=200),
                owner=user,
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Сообщение '{message.subject}' "
                    f"создано для пользователя {user.username}"
                )
            )
