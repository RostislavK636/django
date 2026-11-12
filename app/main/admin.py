from django.contrib import admin

# Register your models here.
from main.models import Course, Category, Recipe

# Добавляем модель в интерфейс администрирования.
admin.site.register(Course)

# Добавляем модель в интерфейс администрирования.
admin.site.register(Category)
# Добавляем модель в интерфейс администрирования.
admin.site.register(Recipe)