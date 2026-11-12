from django import forms
from main.models import Course, Recipe, Category

class CourseForm(forms.ModelForm):
    # Создаём форму ввода данных курса.
    class Meta:
        # Задаём параметры модели или формы.
        # Выбираем модель для построения формы.
        model = Course
        # Перечисляем поля модели, доступные в форме.
        fields = ['name', 'description', 'price', 'image']

class RecipeForm(forms.ModelForm):
    # Создаём форму ввода рецепта и выбора категории.
    class Meta:
        # Задаём параметры модели или формы.
        # Выбираем модель для построения формы.
        model = Recipe
        # Перечисляем поля модели, доступные в форме.
        fields = ['name', 'Category']

class CategoryForm(forms.ModelForm):
    # Создаём форму названия категории.
    class Meta:
        # Задаём параметры модели или формы.
        # Выбираем модель для построения формы.
        model = Category
        # Перечисляем поля модели, доступные в форме.
        fields = ['name']