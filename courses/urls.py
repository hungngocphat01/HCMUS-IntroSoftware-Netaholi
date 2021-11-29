from django.urls import path
from . import views

urlpatterns = [
    path('details/<str:pk>/', views.detail_page_view, name='details'),
]
