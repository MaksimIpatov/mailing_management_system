from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import COUNTRY_NAME_LEN, NULL_BLANK_TRUE, PHONE_NUMBER_LEN


class CustomUser(AbstractUser):
    email = models.EmailField("E-mail", unique=True)
    avatar = models.ImageField(
        "Фото профиля",
        upload_to="avatars/",
        **NULL_BLANK_TRUE,
    )
    phone_number = models.CharField(
        "Номер телефона",
        max_length=PHONE_NUMBER_LEN,
        **NULL_BLANK_TRUE,
    )
    country = models.CharField(
        "Страна",
        max_length=COUNTRY_NAME_LEN,
        **NULL_BLANK_TRUE,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def __str__(self) -> str:
        return self.username
