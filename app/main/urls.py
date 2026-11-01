
from django.urls import path
from main import views

app_name='main'

urlpatterns = [

    path('', views.index, name='index'),
    path('courses/', views.course, name='courses'),
    path('courses/<int:course_id>', views.course_detail, name='course_detail'),
    path('courses/add', views.course_add, name='add'),
    path('courses/<int:course_id>/edit/', views.course_edit, name='course_edit'),
    path('courses/<int:course_id>/restore/', views.course_restore, name='course_restore'),
    path('courses/deleted', views.deleted_course, name='deleted_course'),
    path('courses/<int:course_id>/restore', views.course_deleted, name='course_deleted'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]

