NAME_LEN: int = 30
SUBJECT_LEN: int = 120

MAILING_STATUS: dict[str, str] = {
    "created": "Создана",
    "started": "Запущена",
    "finished": "Завершена",
}

MAIL_SEND_STATUS: dict[str, str] = {
    "success": "Успешно",
    "failure": "Не успешно",
}

SEND_MAILING_HOURS: int = 1
SEND_MAILING_MAX_INSTANCES: int = 1
