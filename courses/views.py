import secrets
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import Course, Material
from .forms import *
from manager.decorators import *
from .decorators import *


# Create your views here.
@login_only
def detail_page_view(req, course_id):
    if req.method == 'GET':
        course = Course.objects.get(id=course_id)
        context = {'course': course}
        return render(req, 'courses/details.html', context)


@login_only
def enroll_view(req: HttpRequest, course_id):
    # Check if user is enrolled
    user = req.user
    course = get_object_or_404(Course, id=course_id)
    if course.is_enrolled(user.username):
        return render(req, 'home/error.html', {'error_message': 'Bạn đã đăng ký vào khóa học này rồi!'})

    if req.method == 'GET':
        # Invoice id is a random 5-byte hex string (for emulation)
        context = {'course': course, 'invoice_id': secrets.token_hex(5)}
        return render(req, 'courses/enroll.html', context)
    elif req.method == 'POST':
        # Check if user checked the "agree" box
        if not req.POST.get('agree-checkbox'):
            messages.error(req, 'Bạn chưa đồng ý với điều khoản của khóa học')
            return redirect('enroll')
        if course.enroll_student(user):
            return redirect(reverse('dashboard', kwargs={'course_id': course_id}))
        else:
            return render(req, 'home/error.html',
                          {'error_message': 'Không thể đăng ký bạn vào khóa học! Vui lòng liên hệ quản trị viên.'})


@enrolled_only
def dashboard_view(req, course_id):
    course = Course.objects.get(id=course_id)
    try:
        materials = Material.objects.filter(course=course)
    except Material.DoesNotExist:
        materials = None
    context = {'course': course, 'materials': materials}
    return render(req, 'courses/dashboard.html', context)


@enrolled_only
def material_view(req, course, course_id):
    course = get_object_or_404(Course, id=course)
    material = get_object_or_404(Material, id=course_id)
    context = {'course': course, 'material': material}
    return render(req, 'courses/material.html', context)


@teacher_admin_only
@enrolled_only
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
        return redirect(reverse('dashboard', kwargs={'course_id': course_id}))


@teacher_admin_only
@enrolled_only
def material_create_edit(req, course_id, material_id):
    course = get_object_or_404(Course, id=course_id)
    material = get_object_or_404(Material, id=material_id)

    if req.method == 'GET':
        print('Edit')
        form = MaterialForm(instance=material)
        context = {'action': 'Sửa đổi', 'form': form, 'course': course}
        return render(req, 'courses/material_create_edit.html', context)
    else:
        form = MaterialForm(req.POST, instance=material)
        if form.is_valid():
            form.save()
        return redirect(reverse('dashboard', kwargs={'course_id': course_id}))

