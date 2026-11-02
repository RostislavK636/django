from django.contrib import admin

# Register your models here.
from main.models import Course, Category, Recipe

admin.site.register(Course)

admin.site.register(Category)
admin.site.register(Recipe)