from django.http import HttpResponse
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from home.models import UserProfile


def login_only(view_func):
    def wrapper(req, *args, **kwargs):
        return view_func(req, *args, **kwargs)
    return login_required(function=wrapper, login_url='login')


def teacher_admin_only(view_func):
    def wrapper(req, *args, **kwargs):
        current_user = req.user
        group = None
        if current_user.groups.exists():
            group = req.user.groups.all()[0].name

        if current_user.is_staff or group == 'Teacher':
            return view_func(req, *args, **kwargs)
        else:
            return HttpResponseForbidden('<h1>403 Forbidden</h1><br><h2>You are not supposed to be here!</h2>')
    return login_only(wrapper)


def admin_only(view_func):
    def wrapper(req, *args, **kwargs):
        current_user = req.user

        if current_user.is_staff:
            return view_func(req, *args, **kwargs)
        else:
            return HttpResponseForbidden('<h1>403 Forbidden</h1><br><h2>You are not supposed to be here!</h2>')
    return login_only(wrapper)

