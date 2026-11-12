#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    # Подготавливаем настройки и запускаем команду Django из терминала.
    """Run administrative tasks."""
    # Выбираем модуль настроек, если он ещё не задан в окружении.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    try:
        # Выполняем операцию с обработкой возможной ошибки ниже.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Объясняем причину остановки при недоступном Django.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Передаём Django команду и аргументы терминала.
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Запускаем команды при прямом выполнении manage.py.
    main()
