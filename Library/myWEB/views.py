from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password  # 用户密码管理
from .models import dzTable, tsglyTable, smTable, tsTable, jsTable, yyTable  # 引入数据库

# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate
# from django.contrib.auth import login, logout


def home(request):
    return render(request, 'home.html')


def login_view(request):  # 读者、管理员用户登录
    context = dict()
    if request.method == 'POST':
        context["username"] = username = request.POST.get("username")
        password = request.POST.get("password")
        if not username:
            context["msg"] = "请输入邮箱、读者id或图书管理员工号"
            return render(request, 'home.html', context=context)
        if not password:
            context["msg"] = "密码不能为空"
            return render(request, 'home.html', context=context)
        if '@' in username:  # 读者使用邮箱登录
            result = dzTable.objects.filter(email=username)
            if result.exists() and check_password(password, result[0].psw):  # 读者邮箱登录成功
                request.session['login_type'] = 'dz'
                request.session['id'] = result[0].dzid
                request.session['xm'] = result[0].xm
                return redirect('/dz_index/')
            else:
                context["msg"] = "密码输入错误"
                return render(request, 'home.html', context=context)
        elif 'gh' in username:  # 管理员使用工号登录
            result = tsglyTable.objects.filter(gh=username)
            if result.exists and password == result[0].psw:  # 管理员登录成功
                request.session['login_type'] = 'gly'
                request.session['id'] = result[0].gh
                request.session['xm'] = result[0].xm
                return redirect('/gly_index/')
            else:
                context["msg"] = "密码输入错误"
                return render(request, 'home.html', context=context)
        else:  # 读者使用id登录
            username = username.lstrip('0')
            result = dzTable.objects.filter(dzid=username)
            if result.exists() and check_password(password, result[0].psw):  # 读者id登录成功
                request.session['login_type'] = 'dz'
                request.session['id'] = result[0].dzid
                request.session['xm'] = result[0].xm
                return redirect('/dz_index/')
            else:
                context["msg"] = "密码输入错误"
                return render(request, 'home.html', context=context)
    else:
        return render(request, 'home.html')


def register(request):  # 新读者注册账户
    context = dict()
    if request.method == 'GET':
        return render(request, 'register.html', context=context)
    elif request.method == 'POST':
        context["xm"] = xm = request.POST.get("xm")  # 姓名
        context["dh"] = dh = request.POST.get("dh")  # 电话
        context["yx"] = yx = request.POST.get("yx")  # 邮箱
        mm = request.POST.get("mm")  # 密码
        mmqr = request.POST.get("mmqr")  # 密码确认
        context["msg"] = "未知错误，请重试"
        if mm != mmqr:
            context["msg"] = "两次密码输入不一致，请检查"
            return render(request, 'register.html', context=context)
        if len(mm) < 6:
            context["msg"] = "密码长度至少需要六位"
            return render(request, 'register.html', context=context)
        if '@' not in yx:
            context["msg"] = "邮箱格式错误"
            return render(request, 'register.html', context=context)
        result = dzTable.objects.filter(email=yx)
        if result.exists():
            context["msg"] = "邮箱已经注册，请点击下方链接登录"
            return render(request, 'register.html', context=context)
        item = dzTable(
            xm=xm,
            dh=dh,
            email=yx,
            psw=make_password(mm)
        )
        item.save()
        result = dzTable.objects.get(email=yx)
        context["msg"] = "注册成功，读者id为：" + str(result.dzid).zfill(5)
        return render(request, 'register.html', context=context)
    else:
        return render(request, 'register.html', context=context)


def logout_view(request):  # 读者、管理员退出登录
    if request.session.get('login_type', None):
        request.session.flush()
    return HttpResponseRedirect("/")


# =====================读者======================


def dz_index(request):  # 读者首页
    if request.session.get('login_type', None) != 'dz':
        return HttpResponseRedirect("/")
    context = dict()
    context['xm'] = request.session.get('xm')
    return render(request, 'dz_index.html', context=context)


def dz_smztcx(request):  # 读者书目状态查询
    if request.session.get('login_type', None) != 'dz':
        return HttpResponseRedirect("/")
    context = dict()
    context['xm'] = request.session.get('xm', None)
    return render(request, 'dz_smztcx.html', context=context)


def dz_yydj(request):  # 读者预约登记(借不到的书)
    if request.session.get('login_type', None) != 'dz':
        return HttpResponseRedirect("/")
    context = dict()
    context['xm'] = request.session.get('xm', None)
    return render(request, 'dz_yydj.html', context=context)


def dz_grztcx(request):  # 读者个人(借书)状态查询
    if request.session.get('login_type', None) != 'dz':
        return HttpResponseRedirect("/")
    context = dict()
    context['xm'] = request.session.get('xm', None)
    result = jsTable.objects.filter(dzid=request.session.get(id))
    grzt = []
    for elem in result:
        grzt.append({'tsid': elem.tsid, 'jysj': elem.jysj, 'yhsj': elem.yhsj, 'ghsj': elem.ghsj})
    context['smzt'] = grzt
    return render(request, 'dz_grztcx.html', context=context)


# =====================管理员======================


def gly_index(request):  # 管理员首页
    if request.session.get('login_type', None) != 'gly':
        return HttpResponseRedirect("/")
    context = dict()
    context['xm'] = request.session.get('xm')
    return render(request, 'gly_index.html', context=context)


def gly_smztcx(request):  # 管理员书目状态查询
    if request.session.get('login_type', None) != 'gly':
        return HttpResponseRedirect("/")
    context = dict()
    context['xm'] = request.session.get('xm')
    return render(request, 'gly_smztcx.html', context=context)


def gly_js(request):  # 管理员借书
    if request.session.get('login_type', None) != 'gly':
        return HttpResponseRedirect("/")
    context = dict()
    context['xm'] = request.session.get('xm')
    return render(request, 'gly_js.html', context=context)


def gly_hs(request):  # 管理员还书
    if request.session.get('login_type', None) != 'gly':
        return HttpResponseRedirect("/")
    context = dict()
    context['xm'] = request.session.get('xm')
    return render(request, 'gly_hs.html', context=context)


def gly_rk(request):  # 管理员入库
    if request.session.get('login_type', None) != 'gly':
        return HttpResponseRedirect("/")
    context = dict()
    context['xm'] = request.session.get('xm')
    return render(request, 'gly_rk.html', context=context)


def gly_ck(request):  # 管理员出库
    if request.session.get('login_type', None) != 'gly':
        return HttpResponseRedirect("/")
    context = dict()
    context['xm'] = request.session.get('xm')
    return render(request, 'gly_ck.html', context=context)
