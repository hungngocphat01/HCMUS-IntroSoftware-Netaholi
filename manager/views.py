from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from courses.models import Course, Material
from courses.forms import *
from .decorators import *


@admin_only
def manager_home_view(req):
    """
    Home view of administration section of the website
    """
    context = {}
    return render(req, 'manager/manager_home.html', context)


@admin_only
def course_create_view(req):
    """
    Create a new course
    """
    if req.method == 'GET':
        form = CourseDetailsForm()
        context = {'action': 'Tạo mới', 'form': form}
        return render(req, 'courses/create_edit.html', context)
    if req.method == 'POST':
        print("POST received")
        form = CourseDetailsForm(req.POST)
        if form.is_valid():
            form.save()
            print('New course created')
        else:
            print('Form invalid!')
        return redirect('home')


@teacher_admin_only
def course_edit_view(req, pk):
    course = Course.objects.get(id=pk)
    form = CourseDetailsForm(instance=course)
    if req.method == 'GET':
        context = {'form': form, 'action': 'Chỉnh sửa thông tin'}
        return render(req, 'courses/create_edit.html', context)
    else:
        form = CourseDetailsForm(req.POST, req.FILES, instance=course)
        if form.is_valid():
            form.save()
            print("Course saved!")
        else:
            print("Form invalid!")
        return redirect('home')
