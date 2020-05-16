from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect

from time import time


def home(request):
    return render(request, 'home.html')


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:  # 登录成功，进入首页
                login(request, user)
                request.session['username'] = username
                return HttpResponseRedirect("/index/")
            else:
                context["msg"] = "用户已被锁定，请联系管理员"
                return render(request, "home.html", context=context)
        else:
            context["msg"] = "用户名或密码错误"
            return render(request, "home.html", context=context)
    else:
        return render(request, 'home.html')


def register(request):  # 新读者注册账户
    return render(request, 'register.html')


def register_submit(request):
    curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ...


@login_required
def logout_view(request):  # 退出登录
    logout(request)
    return HttpResponseRedirect("/")


@login_required
def index(request):  # 首页
    return render(request, 'index.html')
