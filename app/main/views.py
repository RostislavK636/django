from django.shortcuts import render

def index(request):
    context = {
        'title': 'Платформа обучения',
    }
    return render(request, 'main/index.html', context)


def course(request):
    context = {
        'title': 'Мои курсы',
        'course': [],
    }
    return render(request, 'main/course.html', context)
