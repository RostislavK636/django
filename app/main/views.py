from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {
        'title': "Платформа для обучения" 
    }
    return render(request, 'main/index.html', context)
def course(request):
    context = {
        'title': " Мои курсы" , 
        'course': []
    }
    return render(request, 'main/course.html', context)