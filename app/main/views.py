from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse('Платформа обучения')
def course(request):
    context = {
        'title': " Мои курсы" , 
        'course': []
    }
    return render(request, 'main/index.html', context)