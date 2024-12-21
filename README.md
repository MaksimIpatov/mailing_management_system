# ПисьмоХ

---

## Описание проекта

**Письмох** — это веб-приложение для управления рассылками. Сервис позволяет:

- Создавать и управлять рассылками
- Работать с сообщениями
- Управлять получателями рассылок
- Просматривать статистику рассылок

Проект ориентирован на администраторов и менеджеров рассылок, обеспечивая функциональность для выполнения всех этапов
работы с рассылками — от их создания до анализа результатов.

---

## Стек технологий:

- **Python**
- **Django**
- **PostgreSQL**

---

## Как запустить проект

Шаги для локального запуска проекта:

1. **Клонировать репозиторий и перейти в директорию проекта:**

    ```bash
    git clone https://github.com/MaksimIpatov/mailing_management_system.git && cd mailing_management_system
    ```

2. **Создать виртуальное окружение и активировать его:**

    - **Windows**:

      ```commandline
      python -m venv .venv 
      ```

    - **Для MacOS/Linux**:

      ```bash
      python3 -m venv .venv
      ```

   После этого активируйте окружение:

    - **Windows (cmd)**:

      ```commandline
      call .venv\Scripts\activate
      ```

    - **Windows (Git Bash)**:

      ```bash
      source .venv\Scripts\activate
      ```

    - **MacOS/Linux**:

      ```bash
      source .venv/bin/activate
      ```

3. **Установить зависимости:**

    - **Windows**:

      ```commandline
      pip install -r requirements.txt
      ```

    - **MacOS/Linux**:

      ```bash
      pip3 install -r requirements.txt
      ```

4. **Настроить переменные окружения:**

   Скопируйте файл `.env.sample` в `.env` и настройте его согласно вашим параметрам.

5. **Применить миграции:**

    ```bash
    python manage.py migrate
    ```

6. **Генерация случайных данных (опционально):**

   Для генерации тестовых данных необходимо выполнить несколько команд.
   Эти данные могут быть полезны для тестирования функционала рассылок, сообщений и получателей.

   Для генерации случайных данных выполните следующие команды по очереди:

    ```bash
    python3 manage.py generate_users
    python3 manage.py generate_recipients
    python3 manage.py generate_messages
    python3 manage.py generate_mailings
    python3 manage.py generate_mail_attempts
    ```

7. **Запустить сервер:**

    ```bash
    python manage.py runserver
    ```

Сервис будет доступен по адресу: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Интерфейс отправки рассылок

- Запустить команду:

```bash
python3 manage.py send_mailing
```

- Опциональный параметр `mailing_id`

```bash
python3 manage.py send_mailing mailing_id=2
```

---

> Все выполненные задания и критерии для проекта описаны в файле [TASKS.md](TASKS.md).
