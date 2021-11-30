from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from courses.models import Course

from .forms import TeacherSignUpForm, SignUpForm

def home_page_view(req: HttpRequest):
    """
    Homepage view
    """
    all_courses = Course.objects.all()
    context = {'courses': all_courses}
    return render(req, 'home/home.html', context)

def register_page_view(req: HttpRequest):
    """
    Register page
    """
    form = SignUpForm()
    if req.method == 'POST':
        form = SignUpForm(req.POST)
        if form.is_valid():
            user: User = form.save()
            user.refresh_from_db()
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.userprofile.profession = form.cleaned_data.get('profession')
            user.userprofile.department = form.cleaned_data.get('department')
            user.userprofile.birthday = form.cleaned_data.get('birthday')
            user.userprofile.gender = form.cleaned_data.get('gender')
            user.save()
            print('User created!')
        return redirect('home')
    else:
        context = {'form': form}
        return render(req, 'home/register.html', context)

def login_page_view(req: HttpRequest):
    if req.method == 'GET':
        return render(req, 'home/login.html')
    elif req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            print('User authenticated:', username)
            login(req, user)
            return redirect('home')
        else:
            print('Login error')
            messages.error(req, 'Sai tên đăng nhập hoặc mật khẩu')
            return redirect('login')

def logout_page_view(req: HttpRequest):
    logout(req)
    return redirect('login')