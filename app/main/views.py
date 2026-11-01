
from django.http import HttpResponse
from main.models import Course
from django.shortcuts import render, get_object_or_404, redirect
from main.forms import CourseForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def index(request):
    context = {
        'title': "Платформа для обучения" ,
    }
    return render(request, 'main/index.html', context)
def course(request):
    course = Course.objects.filter(is_deleted=False)
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
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('main:courses')
    else:
        form = CourseForm()

    context = {
        'form': form
    }

    return render(request, 'main/course_add.html', context)


def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('main:courses')
    else:
        form = CourseForm(instance=course)
    context = {
        'form': form,
    }
    return render(request, 'main/course_edit.html', context)

def course_restore(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        course.is_deleted = not course.is_deleted
        course.save()

    return redirect('main:courses')

def deleted_course(request):
    courses= Course.objects.filter(is_deleted=True)

    context={
        'courses': courses,
    }
    return render(request, 'main/course_deleted.html', context)

def course_deleted(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id, is_deleted=True,)
        if course.image:
            course.image.delete(save=False)
        course.delete()
    return redirect('main:deleted_course')


def login_view(request):
    error = ''
    if request.method=='POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)
            return redirect('main:courses')
        error = 'Неправильный логин или пароль'
    return render(request, 'main/login.html', {'error': error})

def logout_view(request):
    if request.method == 'POST':
        logout(request)

    return redirect('main:login')