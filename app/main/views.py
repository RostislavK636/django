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
        'course': [
            {
                'name': 'Основы Python',
                'description': 'Практический курс по основам программирования на Python.',
                'price': 4990,
            },
            {
                'name': 'Веб-разработка на Django',
                'description': 'Создание веб-приложений на Python и Django.',
                'price': 6990,
            },
            {
                'name': 'Основы HTML и CSS',
                'description': 'Создание и стилизация современных веб-страниц.',
                'price': 3990,
            },
        ]
    }
    return render(request, 'main/course.html', context)