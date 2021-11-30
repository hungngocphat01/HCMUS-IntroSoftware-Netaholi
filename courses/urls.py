from django.urls import path
from . import views

urlpatterns = [
    path('details/<str:pk>', views.detail_page_view, name='details'),
    path('create/', views.create_view, name='create'),
    path('edit/<str:pk>', views.edit_view, name='edit'),
]
