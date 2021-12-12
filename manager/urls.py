from django.urls import path
from . import views

urlpatterns = [
    path('', views.manager_home_view, name='manager_home'),
    path('create/course', views.course_create_view, name='course_create'),
    path('edit/course/<str:pk>', views.course_edit_view, name='course_edit'),
]
