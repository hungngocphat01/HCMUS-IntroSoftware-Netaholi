from django.contrib import messages
from django.http.request import HttpRequest
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
def manager_courses_view(req):
    courses = Course.objects.all()

    context = {'courses': courses}
    return render(req, 'manager/manager_courses.html', context)

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


@admin_only
def course_edit_view(req, course_id):
    course = Course.objects.get(id=course_id)
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

@admin_only
def course_delete_view(req: HttpRequest, course_id):
    course = get_object_or_404(Course, id=course_id)

    if req.method == 'GET':
        context = {'course': course}
        return render(req, 'courses/delete.html', context)
    elif req.method == 'POST':
        course.delete()
        course_name = course.name
        messages.info(req, f"Khóa học đã được xóa: {course_name}")
        return redirect(req, 'manager_courses')
