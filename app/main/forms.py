from django import forms
from main.models import Course, Recipe, Category

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'price', 'image']

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name', 'Category']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']