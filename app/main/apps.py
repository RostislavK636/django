from django.apps import AppConfig


class MainConfig(AppConfig):
    # Настраиваем подключение приложения main.
    # Выбираем тип автоматических идентификаторов моделей приложения.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
