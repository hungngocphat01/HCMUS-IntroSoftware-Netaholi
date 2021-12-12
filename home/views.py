from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
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


def account_register_view(req: HttpRequest, account_type):
    """
    Register page
    """
    if account_type == 'teacher':
        form = TeacherSignUpForm()
    else:
        form = SignUpForm()

    if req.method == 'POST':
        if account_type == 'teacher':
            form = TeacherSignUpForm(req.POST)
        else:
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
            # If account is teacher => extra information
            if account_type == 'teacher':
                user.userprofile.bio = form.cleaned_data.get('bio')
                user.userprofile.is_teacher = True
                user.is_active = False
            user.userprofile.gender = form.cleaned_data.get('gender')
            user.save()
            print('User created!')
        else:
            return render(req, 'home/error.html',
                          {'error_message': 'Thông tin bạn đã nhập không hợp lệ'})
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


def choose_acc_register_view(req: HttpRequest):
    return render(req, 'home/register_choose.html')
