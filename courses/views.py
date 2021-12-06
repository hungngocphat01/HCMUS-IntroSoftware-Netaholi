from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .models import Course, Material
from .forms import *
from .decorators import *


# Create your views here.
@login_only
def detail_page_view(req, pk):
    if req.method == 'GET':
        course = Course.objects.get(id=pk)
        context = {'course': course}
        return render(req, 'courses/details.html', context)


@admin_only
def create_view(req):
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
def edit_view(req, pk):
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


def dashboard_view(req, pk):
    course = Course.objects.get(id=pk)
    try:
        materials = Material.objects.filter(course=course)
    except Material.DoesNotExist:
        materials = None
    context = {'course': course, 'materials': materials}
    return render(req, 'courses/dashboard.html', context)


def material_view(req, course, pk):
    course = get_object_or_404(Course, id=course)
    material = get_object_or_404(Material, id=pk)
    context = {'course': course, 'material': material}
    return render(req, 'courses/material.html', context)


def material_create_view(req, course_id):
    course = get_object_or_404(Course, id=course_id)
    if req.method == 'GET':
        form = MaterialForm(initial={'course': course})
        context = {'action': 'Tạo mới', 'form': form, 'course': course}
        return render(req, 'courses/material_create_edit.html', context)
    else:
        form = MaterialForm(req.POST)
        if form.is_valid():
            new_material: Material = form.save(commit=False)
            new_material.course = course
            new_material.save()
        return redirect(reverse('dashboard', kwargs={'pk': course_id}))


def material_create_edit(req, course_id, pk):
    course = get_object_or_404(Course, id=course_id)
    material = get_object_or_404(Material, id=pk)

    if req.method == 'GET':
        print('Edit')
        form = MaterialForm(instance=material)
        context = {'action': 'Sửa đổi', 'form': form, 'course': course}
        return render(req, 'courses/material_create_edit.html', context)
    else:
        form = MaterialForm(req.POST, instance=material)
        if form.is_valid():
            form.save()
        return redirect(reverse('dashboard', kwargs={'pk': course_id}))



