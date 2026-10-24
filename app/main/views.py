from django.shortcuts import render
from django.http import HttpResponse
from main.models import Course
# Create your views here.
def index(request):
    course = Course.objects.all()
    context = {
        'title': "Платформа для обучения" ,
        
    }
    return render(request, 'main/index.html', context)
def course(request):
    context = {
        'title': " Мои курсы" , 
        'course': course}
    return render(request, 'main/course.html', context)