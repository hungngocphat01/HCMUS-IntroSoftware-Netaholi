from django.urls import path
from . import views

urlpatterns = [
    path('', views.manager_home_view, name='manager_home'),
    path('course', views.manager_courses_view, name='manager_course'),
    path('create/course', views.course_create_view, name='course_create'),
    path('edit/course/<str:course_id>', views.course_edit_view, name='course_edit'),
    path('delete/course/<str:course_id>', views.course_delete_view, name='course_delete'),
]
