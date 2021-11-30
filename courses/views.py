from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Course
from .forms import *
from .decorators import *

# Create your views here.
@login_required(login_url='login')
def detail_page_view(req, pk):
    if req.method == 'GET':
        course = Course.objects.get(id=pk)
        context = {'course': course}
        return render(req, 'courses/details.html', context)

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