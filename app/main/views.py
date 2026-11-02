
from django.http import HttpResponse
from main.models import Course, Recipe, Category
from django.shortcuts import render, get_object_or_404, redirect
from main.forms import CourseForm, RecipeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
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

@staff_member_required(login_url='main:login')
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

@staff_member_required(login_url='main:login')
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

@staff_member_required(login_url='main:login')
def course_restore(request, course_id):
    if request.method == 'POST':
        course = get_object_or_404(Course, id=course_id)
        course.is_deleted = not course.is_deleted
        course.save()

    return redirect('main:courses')

@staff_member_required(login_url='main:login')
def deleted_course(request):
    courses= Course.objects.filter(is_deleted=True)

    context={
        'courses': courses,
    }
    return render(request, 'main/course_deleted.html', context)

@staff_member_required(login_url='main:login')
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


def recipe(request):
    category_id = request.GET.get('category', '')
    recipe = Recipe.objects.all()
    if category_id.isdecimal():
        recipe = Recipe.objects.filter(Category_id = category_id)
    context ={
        'title': "Список курсов",
        'recipe': recipe,
        'categories': Category.objects.all()
    }
    return render(request, 'main/recipe.html', context)

@staff_member_required(login_url='main:login')
def recipe_add(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('main:recipe')
    else:
        form = RecipeForm()

    context = {
        'form': form
    }
    return render(request, 'main/recipe_add.html', context)

@staff_member_required(login_url='main:login')
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)

        if form.is_valid():
            form.save()
            return redirect('main:recipe')
    else:
        form = RecipeForm(instance=recipe)
    context = {
        'form': form
    }
    return render(request, 'main/recipe_edit.html', context)


def recipe_filter(request, name_category):
    if request.method == 'POST':
        form = Recipe.objects.filter(Category = name_category)
    context = {
        'recipe': recipe
    }    
    return redirect(request, 'main:recipe', context)
