
from django.urls import path
from main import views

app_name='main'

urlpatterns = [

    path('', views.index, name='index'),
    path('courses/', views.course, name='courses'),
    path('courses/<int:course_id>', views.course_detail, name='course_detail'),
    path('course/add', views.course_add, name='add'),
]

