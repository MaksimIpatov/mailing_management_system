from django.db import models

from senders.constants import (
    MAIL_SEND_STATUS,
    MAILING_STATUS,
    NAME_LEN,
    SUBJECT_LEN,
)
from users.models import CustomUser


class Recipient(models.Model):
    email = models.EmailField(
        "E-mail",
        unique=True,
    )
    first_name = models.CharField(
        "Имя",
        max_length=NAME_LEN,
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=NAME_LEN,
    )
    middle_name = models.CharField(
        "Отчество",
        max_length=NAME_LEN,
        blank=True,
    )
    comment = models.TextField(
        "Комментарий",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="recipients",
    )

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ("first_name", "last_name")
        permissions = [
            ("can_edit_recipient", "Можнет редактировать получателя"),
            ("can_delete_recipient", "Может удалить получателя"),
        ]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Message(models.Model):
    subject = models.CharField(
        "Тема",
        max_length=SUBJECT_LEN,
    )
    body = models.TextField(
        "Текст",
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="messages",
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ("subject",)
        permissions = [
            ("can_edit_message", "Может редактировать сообщение"),
            ("can_delete_message", "Может удалить сообщение"),
        ]

    def __str__(self) -> str:
        return str(self.subject)


class Mailing(models.Model):
    start_date = models.DateTimeField(
        "Время отправки",
        null=True,
    )
    end_date = models.DateTimeField(
        "Время окончания",
        null=True,
    )
    status = models.CharField(
        "Статус",
        choices=tuple(MAILING_STATUS.items()),
        default="created",
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="mailings",
        verbose_name="Сообщение",
    )
    recipients = models.ManyToManyField(
        Recipient,
        related_name="mailings",
        verbose_name="Получатели",
    )
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="mailings",
    )
    success_count = models.IntegerField("Успешно", default=0)
    failure_count = models.IntegerField("Не успешно", default=0)

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = (
            "-start_date",
            "-end_date",
            "status",
        )
        permissions = [
            (
                "can_manage_own_mailings",
                "Может управлять собственными рассылками",
            ),
            ("can_manage_all_mailings", "Может управлять всеми рассылками"),
        ]

    def get_mail_attempts(self):
        return MailAttemptToSend.objects.filter(mailing=self)

    def update_statistics(self):
        attempts = self.get_mail_attempts()
        self.success_count = attempts.filter(
            status=MAIL_SEND_STATUS["success"],
        ).count()
        self.failure_count = attempts.filter(
            status=MAIL_SEND_STATUS["failure"],
        ).count()
        self.save()

    def __str__(self) -> str:
        return f"{self.start_date} - {self.end_date} | [{self.status}]"


class MailAttemptToSend(models.Model):
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Рассылка",
    )
    attempt_date = models.DateTimeField(
        "Дата и время",
        auto_now_add=True,
    )
    status = models.CharField(
        "Статус",
        choices=tuple(MAIL_SEND_STATUS.items()),
    )
    server_response = models.TextField(
        "Ответ почтового сервера",
        default="Успешно",
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ("-attempt_date", "status")

    def __str__(self) -> str:
        return f"{self.mailing.owner.first_name} [{self.status}]"
