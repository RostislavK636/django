from django.shortcuts import render
from django.http import HttpResponse
from main.models import Course
# Create your views here.
def index(request):
    
    context = {
        'title': "Платформа для обучения" ,
        
    }
    return render(request, 'main/index.html', context)
def course(request):
    course = Course.objects.filter(price__gte=10)
    context = {
        
        'title': " Мои курсы" , 
        'course': course}
    return render(request, 'main/course.html', context)