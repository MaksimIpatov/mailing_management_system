import random

from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from faker import Faker

from users.models import CustomUser

fake = Faker()


class Command(BaseCommand):
    help = "Генерация случайных пользователей с разными ролями"

    def handle(self, *args, **kwargs):
        number_of_users = 20
        manager_group, _ = Group.objects.get_or_create(name="Менеджер")
        user_group, _ = Group.objects.get_or_create(name="Пользователь")

        for _ in range(number_of_users):
            user = CustomUser.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=settings.DEFAULT_PASSWORD_FOR_TEST_USERS,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
            )

            role = random.choice(["user", "admin", "superuser"])
            if role == "superuser":
                user.is_superuser = True
                user.is_staff = True
            elif role == "admin":
                user.groups.add(manager_group)
            else:
                user.groups.add(user_group)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Пользователь {user.username} с ролью {role} создан"
                )
            )
