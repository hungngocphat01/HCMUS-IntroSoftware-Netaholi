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
    context = {}
    if account_type == 'teacher':
        form = TeacherSignUpForm()
        context['role'] = 'giảng viên'
    else:
        form = SignUpForm()
        context['role'] = 'học viên'

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
            user.userprofile.gender = form.cleaned_data.get('gender')
            # If account is teacher => extra information
            if account_type == 'teacher':
                user.userprofile.bio = form.cleaned_data.get('bio')
                user.userprofile.is_teacher = True
                user.is_active = False
                messages.warning(req, 'Tài khoản của bạn đã được tạo, vui lòng đợi xác nhận từ phía hệ thống.')
            else:
                messages.info(req, 'Tài khoản của bạn đã được tạo!')
            user.save()

            return redirect('login')
        
    context['form'] = form
    return render(req, 'home/register.html', context)


def login_page_view(req: HttpRequest):
    """
    Login page of the website
    """
    if req.method == 'GET':
        return render(req, 'home/login.html')
    elif req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')

        # Check user is locked
        try:
            user: User = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(req, 'Tên đăng nhập không tồn tại trên hệ thống')
            return redirect('login')
        
        if not user.is_active:
            if user.userprofile.is_teacher:
                messages.error(req, 'Tài khoản của bạn đang chờ QTV xác nhận.')
            else:
                messages.error(req, 'Tài khoản của bạn đã bị đình chỉ. Vui lòng liên hệ QTV.')
            return redirect('login')

        user = authenticate(username=username, password=password)
        if user is not None:
            print('User authenticated:', username)
            login(req, user)
            return redirect('home')
        else:
            print('Login error')
            messages.error(req, 'Sai mật khẩu')
            return redirect('login')


def logout_page_view(req: HttpRequest):
    logout(req)
    return redirect('login')


def choose_acc_register_view(req: HttpRequest):
    return render(req, 'home/register_choose.html')
