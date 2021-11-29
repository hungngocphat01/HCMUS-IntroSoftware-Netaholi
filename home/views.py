from django.shortcuts import render
from .models import Course

def home_page_view(req):
    """
    Homepage view
    """
    all_courses = Course.objects.all()
    context = {'courses': all_courses}
    return render(req, 'home/home.html', context)