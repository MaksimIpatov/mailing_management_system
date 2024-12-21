import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django.utils import timezone
from django_apscheduler.jobstores import DjangoJobStore

from senders.constants import SEND_MAILING_HOURS, SEND_MAILING_MAX_INSTANCES
from senders.models import MailAttemptToSend, Mailing

logger = logging.getLogger(__name__)


def send_mailing(mailing=None):
    if mailing:
        mailings = [mailing]
    else:
        mailings = Mailing.objects.filter(
            status="started",
            end_date__gt=timezone.now(),
        )

    for mailing in mailings:
        for recipient in mailing.recipients.all():
            try:
                send_mail(
                    subject=mailing.message.subject,
                    message=mailing.message.body,
                    from_email="from@pismox.ru",
                    recipient_list=[recipient.email],
                )
                MailAttemptToSend.objects.create(
                    mailing=mailing,
                    status="success",
                    server_response="Успешно",
                )
            except Exception as err:
                MailAttemptToSend.objects.create(
                    mailing=mailing,
                    status="failure",
                    server_response="Отказ",
                )
        mailing.update_statistics()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        send_mailing,
        "interval",
        hours=SEND_MAILING_HOURS,
        id="send_mailing_job",
        max_instances=SEND_MAILING_MAX_INSTANCES,
        replace_existing=True,
    )

    scheduler.start()
