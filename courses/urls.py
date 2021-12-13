from django.urls import path
from . import views

urlpatterns = [
    path('details/<str:course_id>', views.detail_page_view, name='details'),
    path('enroll/<str:course_id>', views.enroll_view, name='enroll'),
    path('dashboard/<str:course_id>', views.dashboard_view, name='dashboard'),
    path('lesson/<str:course_id>', views.lesson_view, name='lesson'),
    path('dashboard/<str:course_id>/material/create', views.material_create_view, name='material_create'),
    path('dashboard/<str:course>/material/<str:material_id>', views.material_view, name='material'),
    path('dashboard/<str:course_id>/material/edit/<str:material_id>',
         views.material_create_edit, name='material_edit'),
]
