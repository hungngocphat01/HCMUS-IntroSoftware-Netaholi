from django.urls import path
from . import views

urlpatterns = [
    path('details/<str:pk>', views.detail_page_view, name='details'),
    path('dashboard/<str:pk>', views.dashboard_view, name='dashboard'),
    path('dashboard/<str:course_id>/material/create', views.material_create_view, name='material_create'),
    path('dashboard/<str:course>/material/<str:pk>', views.material_view, name='material'),
    path('dashboard/<str:course_id>/material/edit/<str:pk>', views.material_create_edit, name='material_edit'),
    path('create/', views.create_view, name='create'),
    path('edit/<str:pk>', views.edit_view, name='edit'),
]
