from django import template

from senders.constants import MAILING_STATUS

register = template.Library()


@register.filter
def status_display(value: str) -> str:
    """
    Отображает строковое отображение статуса рассылки.
    :param value: Статус в виде ключа (напр., "created").
    :return: Отображаемое название статуса.
    """
    return MAILING_STATUS.get(value, value)
