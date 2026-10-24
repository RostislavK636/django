
from django.urls import path
from main import views

app_name='main'

urlpatterns = [

    path('', views.index, name='index'),
    path('courses/', views.course, name='courses'),
]