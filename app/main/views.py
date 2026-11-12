
# Импортируем модели, формы и инструменты Django, которые используются ниже.
from django.http import HttpResponse
from main.models import Course, Recipe, Category
from django.shortcuts import render, get_object_or_404, redirect
from main.forms import CourseForm, RecipeForm, CategoryForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

# Импортируем JsonResponse и json для работы с API.
from django.http import JsonResponse
import json

# Получаем активную модель пользователя проекта для регистрации.
from django.contrib.auth import get_user_model
User = get_user_model()

# Подключаем проверку корректности адреса электронной почты.
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# Подключаем регулярные выражения для проверки пароля.
import re

# Показываем главную страницу приложения.
def index(request):
    # Формируем данные, которые будут переданы в HTML-шаблон.
    context = {
        'title': "Платформа для обучения" ,
    }
    # Рендерим главную страницу с подготовленными данными.
    return render(request, 'main/index.html', context)

# Показываем список неудалённых курсов.
def course(request):
    # Получаем только курсы, которые не помечены как удалённые.
    course = Course.objects.filter(is_deleted=False)
    # Передаём список курсов и заголовок в шаблон.
    context = {    
        'title': " Мои курсы" , 
        'course': course}
    # Возвращаем страницу со списком курсов.
    return render(request, 'main/course.html', context)

# Показываем подробную информацию о выбранном курсе.
def course_detail(request, course_id):
    # Ищем курс по идентификатору или возвращаем страницу 404.
    course = get_object_or_404(Course, id=course_id)

    # Подготавливаем данные выбранного курса для шаблона.
    context = {
        'title': course.name,
        'course': course,
    }
    # Рендерим страницу с подробностями курса.
    return render(request, 'main/course_detail.html', context)

@staff_member_required(login_url='main:login')
# Добавляем новый курс через форму.
def course_add(request):
    # Для POST загружаем данные формы и прикреплённый файл.
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)

        # Проверяем форму и сохраняем курс при корректных данных.
        if form.is_valid():
            form.save()
            # После сохранения возвращаемся к списку курсов.
            return redirect('main:courses')
    else:
        # Для GET создаём пустую форму добавления курса.
        form = CourseForm()

    # Передаём форму в шаблон, включая ошибки валидации.
    context = {
        'form': form
    }

    # Показываем страницу добавления курса.
    return render(request, 'main/course_add.html', context)

@staff_member_required(login_url='main:login')
# Редактируем существующий курс.
def course_edit(request, course_id):
    # Находим курс, который нужно изменить.
    course = get_object_or_404(Course, id=course_id)
    # При отправке формы обновляем найденный курс.
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        # Проверяем новые данные и сохраняем изменения.
        if form.is_valid():
            form.save()
            return redirect('main:courses')
    else:
        # При открытии страницы заполняем форму текущими данными курса.
        form = CourseForm(instance=course)
    # Передаём форму редактирования в шаблон.
    context = {
        'form': form,
    }
    # Показываем страницу редактирования курса.
    return render(request, 'main/course_edit.html', context)

@staff_member_required(login_url='main:login')
# Восстанавливаем или помечаем курс как удалённый.
def course_restore(request, course_id):
    # Меняем состояние удаления только после отправки POST-запроса.
    if request.method == 'POST':
        # Находим курс, который нужно восстановить или удалить.
        course = get_object_or_404(Course, id=course_id)
        # Инвертируем текущий признак удаления.
        course.is_deleted = not course.is_deleted
        # Сохраняем новое состояние курса в базе данных.
        course.save()

    # Возвращаем пользователя к списку курсов.
    return redirect('main:courses')

@staff_member_required(login_url='main:login')
# Показываем список курсов, помеченных как удалённые.
def deleted_course(request):
    # Выбираем только удалённые курсы.
    courses= Course.objects.filter(is_deleted=True)

    # Передаём список удалённых курсов в шаблон.
    context={
        'courses': courses,
    }
    # Рендерим страницу удалённых курсов.
    return render(request, 'main/course_deleted.html', context)

@staff_member_required(login_url='main:login')
# Полностью удаляем курс из базы данных.
def course_deleted(request, course_id):
    # Выполняем удаление только для POST-запроса.
    if request.method == 'POST':
        # Ищем только курс, уже помеченный как удалённый.
        course = get_object_or_404(Course, id=course_id, is_deleted=True,)
        # Удаляем связанное изображение, если оно существует.
        if course.image:
            course.image.delete(save=False)
        # Удаляем сам курс из базы данных.
        course.delete()
    # Возвращаемся к списку удалённых курсов.
    return redirect('main:deleted_course')


# Обрабатываем вход пользователя в систему.
def login_view(request):
    # Храним сообщение об ошибке для передачи в шаблон.
    error = ''
    # Обрабатываем только отправленную форму входа.
    if request.method=='POST':
        # Получаем логин и пароль из данных формы.
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # Проверяем учётные данные через стандартный механизм Django.
        user = authenticate(
            request,
            username=username,
            password=password,
        )

        # При успешной проверке создаём сессию пользователя.
        if user is not None:
            login(request, user)
            return redirect('main:courses')
        # Показываем ошибку, если логин или пароль неверны.
        error = 'Неправильный логин или пароль'
    # Показываем форму входа и возможную ошибку.
    return render(request, 'main/login.html', {'error': error})

# Завершаем пользовательскую сессию.
def logout_view(request):
    # Выходим из системы только по POST-запросу.
    if request.method == 'POST':
        logout(request)

    # После выхода направляем пользователя на страницу входа.
    return redirect('main:login')


# Показываем и фильтруем список рецептов.
def recipe(request):
    # Получаем идентификатор категории из параметров URL.
    category_id = request.GET.get('category', '')
    # Начинаем с полного списка рецептов.
    recipe = Recipe.objects.all()
    # Получаем поисковую строку и убираем лишние пробелы.
    search = request.GET.get('search', '').strip()
    # Если пользователь ввёл поиск, оставляем подходящие названия.
    if search:
        recipe = recipe.filter(name__icontains=search)
    # Если идентификатор категории является числом, фильтруем рецепты по ней.
    if category_id.isdecimal():
        recipe = recipe.objects.filter(Category_id = category_id)
    # Выводим диагностическую информацию о применённых фильтрах.
    print('Всего рецептов:', Recipe.objects.count())
    print('После фильтров:', recipe.count())
    print('Поиск:', search, 'Категория:', category_id)
    print(list(Recipe.objects.values_list('name', flat=True)))
    # Формируем контекст для страницы рецептов.
    context ={
        'title': "Список курсов",
        'recipe': recipe,
        'categories': Category.objects.all(),
        'search': search,
        'category_id': category_id,
    }
    # Рендерим список рецептов и доступных категорий.
    return render(request, 'main/recipe.html', context)

@staff_member_required(login_url='main:login')
# Добавляем новый рецепт.
def recipe_add(request):
    # При POST заполняем форму данными запроса.
    if request.method == "POST":
        form = RecipeForm(request.POST)

        # Проверяем форму и сохраняем рецепт при успехе.
        if form.is_valid():
            form.save()
            return redirect('main:recipe')
    else:
        # Для GET создаём пустую форму рецепта.
        form = RecipeForm()

    # Передаём форму в шаблон.
    context = {
        'form': form
    }
    # Показываем страницу добавления рецепта.
    return render(request, 'main/recipe_add.html', context)

@staff_member_required(login_url='main:login')
# Редактируем существующий рецепт.
def recipe_edit(request, recipe_id):
    # Получаем рецепт по идентификатору или возвращаем 404.
    recipe = get_object_or_404(Recipe, id=recipe_id)
    # Обрабатываем отправленную форму редактирования.
    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)

        # Проверяем и сохраняем изменения рецепта.
        if form.is_valid():
            form.save()
            return redirect('main:recipe')
    else:
        # Заполняем форму текущими данными рецепта.
        form = RecipeForm(instance=recipe)
    # Передаём форму в шаблон редактирования.
    context = {
        'form': form
    }
    # Показываем страницу редактирования рецепта.
    return render(request, 'main/recipe_edit.html', context)

@staff_member_required(login_url='main:login')
# Добавляем новую категорию.
def category_add(request):
    # Получаем данные формы при отправке POST-запроса.
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Проверяем форму и сохраняем категорию.
        if form.is_valid():
            form.save()
            return redirect('main:recipe')
    else: 
        # Для GET создаём пустую форму категории.
        form = CategoryForm()
    # Передаём форму в шаблон.
    context = {
        'form': form
    }
    # Показываем страницу добавления категории.
    return render(request, 'main/category_add.html', context)

@staff_member_required(login_url='main:login')
# Редактируем существующую категорию.
def category_edit(request, category_id):
    # Находим категорию по идентификатору.
    category = get_object_or_404(Category, id=category_id)
    # Обрабатываем отправленную форму изменения категории.
    if request.method == 'POST':
        form= CategoryForm(request.POST, instance=category)
        
        # Сохраняем категорию, если форма прошла проверку.
        if form.is_valid():
            form.save()
            # Показываем пользователю сообщение об успешном изменении.
            messages.success(request, 'Успешно изменена')
            return redirect('main:recipe')
    else: 
        # Заполняем форму текущими данными категории.
        form = CategoryForm(instance=category)
    # Передаём форму в шаблон.
    context = {
        'form': form
    }
    # Показываем страницу редактирования категории.
    return render(request, 'main/category_edit.html', context)

@staff_member_required(login_url='main:login')
# Удаляем категорию, если в ней нет рецептов.
def category_delete(request, category_id):
    # Находим категорию или возвращаем страницу 404.
    category = get_object_or_404(Category, id=category_id)
    # Разрешаем удаление только по POST-запросу.
    if request.method == 'POST':
        # Проверяем, используются ли рецепты этой категорией.
        if Recipe.objects.filter(Category_id=category.id).exists():
            # Сообщаем пользователю, почему категорию нельзя удалить.
            messages.error(request, "Нельзя удалить категорию, в ней есть рецепты")
        else: 
            # Сообщаем об успешном удалении и удаляем категорию.
            messages.success(request, 'Категория удалена')
            category.delete()
    # Возвращаем пользователя к списку рецептов.
    return redirect('main:recipe')
        



# Обрабатываем API-запросы для списка и создания рецептов.
def recipe_api(request):
    # Для GET возвращаем все рецепты в формате JSON.
    if request.method == 'GET':
        # Загружаем рецепты из базы данных.
        recipe = Recipe.objects.all()

        # Создаём список данных для JSON-ответа.
        data = []

        # Преобразуем каждый объект рецепта в словарь.
        for item in recipe:
            data.append({
                'id': item.pk,
                'name': item.name,
            })
        # Возвращаем список рецептов клиенту API.
        return JsonResponse({'recipe': data})
    # Для POST создаём новый рецепт из JSON-данных запроса.
    if request.method == 'POST':
        # Преобразуем тело запроса из JSON в словарь Python.
        data = json.loads(request.body)
        # Получаем название рецепта и идентификатор его категории.
        name= data.get('name')
        category_id = data.get('category_id')
        # Проверяем, что название было передано.
        if not name:
            return JsonResponse(
                {'error': 'Введите название'},
                status=400
            )
        # Ограничиваем максимальную длину названия.
        if len(name)> 20:
            return JsonResponse(
                {'error': 'Название слишком длинное'},
                status =400
            )
        # Проверяем, что идентификатор категории является целым числом.
        if type(category_id) is not int:
            return JsonResponse(
                {'error': 'ID категории должен быть целым числом'},
                status=400
            )
        # Проверяем существование указанной категории.
        if not Category.objects.filter(pk=category_id).exists():
            return JsonResponse(
                {'error': 'Категория не найдена'},
            status=400
            )
        # Создаём рецепт после прохождения всех проверок.
        recipe = Recipe.objects.create(
            name=name,
            Category_id=category_id
        )
        # Возвращаем данные созданного рецепта и статус 201.
        return JsonResponse(
            { 'id': recipe.pk, 'name': recipe.name},
            status = 201
        )

# Возвращаем один рецепт по его идентификатору через API.
def recipe_detail_api(request, pk):
    # Пытаемся найти рецепт в базе данных.
    try:
        recipe = Recipe.objects.get(pk=pk)
    # Возвращаем ошибку, если рецепт не найден.
    except Recipe.DoesNotExist:
        return JsonResponse(
            { 'error': 'Рецепт не найден'},
            status =404
        )
    # Возвращаем найденный рецепт в формате JSON.
    return JsonResponse({'id': recipe.pk, 'name': recipe.name})

# Обрабатываем регистрацию пользователя через API.
def register_api(request):
    # Обрабатываем только POST-запрос с данными регистрации.
    if request.method == 'POST':
        # Преобразуем JSON-тело запроса в словарь.
        data = json.loads(request.body)

        # Получаем email и пароль из полученных данных.
        email = data.get('email', '')
        password = data.get('password', '')

        # Создаём словарь для накопления ошибок валидации.
        errors = {}

        # Проверяем наличие и корректность email.
        if not email:
            errors['email'] = ['Введите email']
        else: 
            try:
                # Проверяем формат адреса электронной почты.
                validate_email(email)
            except ValidationError:
                # Записываем ошибку, если формат email неверный.
                errors['email'] = ['Введите корректный email']
        # Проверяем, не зарегистрирован ли такой email ранее.
        if 'email' not in errors:
            if User.objects.filter(email__iexact = email).exists():
                errors['email'] = ['Этот email уже зарегестрирован']
        # Проверяем наличие и минимальную длину пароля.
        if not password:
            errors['password'] = ['Введите пароль']
        elif len(password) < 5:
            errors['password'] = ['Минимум 5 символов']
        # Проверяем наличие строчной латинской буквы.
        elif not re.search(r'[a-z]', password):
            errors['password'] = ['Жобавьте маленькую латинскую букву']
        # Проверяем наличие заглавной латинской буквы.
        elif not re.search(r'[A-Z]', password):
            errors['password'] = ['Добавьте большую букву']
        elif not re.search(r'[#_$-]', password):
            errors['password'] = ['Добавьте один из символов: # _ - $']
        elif not password.isascii():
            errors['password'] = ['Используйте латинские буквы, цифры и обычные знаки']
        # Возвращаем клиенту все найденные ошибки.
        if errors:
            return JsonResponse({
                'message': 'Invalid fields',
                'errors': errors,
            }, status=422)
        User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        return JsonResponse(
            { 'success': True},
            status=201
        )
        
