from django.db import models

# Create your models here.

class Course(models.Model):
    # Описываем сведения о курсе и признак корзины.
    # Храним название с указанным ограничением длины.
    name = models.CharField(max_length = 30, unique=True )
    # Храним необязательное описание курса.
    description = models.CharField(max_length=100, blank=True, null=True)
    # Храним стоимость с двумя знаками после запятой.
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # Сохраняем изображение в папку courses.
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    # Отмечаем перемещение в корзину без удаления записи.
    is_deleted = models.BooleanField(default=False)
    def __str__(self):
        # Возвращаем название для отображения объекта в формах и админке.
        return self.name

    class Meta:
        # Задаём параметры модели или формы.
        # Задаём имя таблицы курсов.
        db_table = 'course'


class Category(models.Model):
    # Храним категории рецептов.
    # Храним название с указанным ограничением длины.
    name = models.CharField(max_length=40, unique=True)
    def __str__(self):
        # Возвращаем название для отображения объекта в формах и админке.
        return self.name

class Recipe(models.Model):
    # Храним рецепт и его связь с категорией.
    # Храним название с указанным ограничением длины.
    name = models.CharField(max_length=20)
    # Связываем рецепт с категорией и защищаем используемую категорию от удаления.
    Category = models.ForeignKey(Category, on_delete=models.PROTECT)
    def __str__(self):
        # Возвращаем название для отображения объекта в формах и админке.
        return self.name