
from django.http import HttpResponse
from main.models import Course
from django.shortcuts import render, get_object_or_404
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

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    context = {
        'title': course.name,
        'course': course,
    }
    return render(request, 'main/course_detail.html', context)

def course_add(request):
    return render(request, 'main/course_add.html')