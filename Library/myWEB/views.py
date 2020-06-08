from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password  # 用户密码管理
from .models import dzTable, tsglyTable, smTable, tsTable, jsTable, yyTable  # 引入数据库

import smtplib  # 邮件服务
from email.mime.text import MIMEText  # 邮件服务
from email.utils import formataddr  # 邮件服务

from time import sleep
from django.utils import timezone  # django带时区管理的时间类


def mail(title, content, coding_type='HTML', retry_flag=False):
    my_sender = ''  # 发件人邮箱账号
    my_pass = ''  # 发件人邮箱口令
    my_user = ''  # 收件人邮箱账号
    really_mail = False
    print('标题：' + title + '\n正文：' + content + '\n')
    if not really_mail:
        return
    while True:
        try:
            msg = MIMEText(content, coding_type, 'utf-8')
            msg['From'] = formataddr(['Lemon', my_sender])
            msg['To'] = formataddr(['Lemon', my_user])
            msg['Subject'] = title
            server = smtplib.SMTP_SSL('smtp.qq.com', 465)
            server.login(my_sender, my_pass)
            server.sendmail(my_sender, [my_user, ], msg.as_string())
            server.quit()
        except Exception as err:
            print('in mailing ', err)
            if not retry_flag:
                break
            sleep(5)
            continue
        return


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
                context["msg"] = "账号或密码输入错误"
                return render(request, 'home.html', context=context)
        elif 'gh' in username:  # 管理员使用工号登录
            result = tsglyTable.objects.filter(gh=username)
            if result.exists and password == result[0].psw:  # 管理员登录成功
                request.session['login_type'] = 'gly'
                request.session['id'] = result[0].gh
                request.session['xm'] = result[0].xm
                return redirect('/gly_index/')
            else:
                context["msg"] = "账号或密码输入错误"
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
                context["msg"] = "账号或密码输入错误"
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
    if request.method == 'GET':
        return render(request, 'dz_smztcx.html', context=context)
    else:
        context['sm'] = sm = request.POST.get('sm')  # 书名
        context['zz'] = zz = request.POST.get('zz')  # 作者
        context['isbn'] = isbn = request.POST.get('isbn')  # ISBN
        context['cbs'] = cbs = request.POST.get('cbs')  # 出版社
        context['msg'] = "未知错误，请重试"
        result = smTable.objects.all()
        if not sm and not zz and not isbn and not cbs:
            context['msg'] = "请输入有效筛选信息！"
            return render(request, 'dz_smztcx.html', context=context)
        if sm:
            result = result.filter(sm__contains=sm)
        if zz:
            result = result.filter(zz__contains=zz)
        if isbn:
            result = result.filter(isbn__startswith=isbn)
        if cbs:
            result = result.filter(cbs__contains=cbs)
        smzt = []
        for elem in result:
            smzt.append(
                {
                    'ISBN': elem.isbn,
                    'sm': elem.sm,
                    'zz': elem.zz,
                    'cbs': elem.cbs,
                    'cbny': elem.cbny,
                    'kccs': len(tsTable.objects.filter(isbn=elem.isbn)),
                    'bwjcs': len(tsTable.objects.filter(zt='不外借')),
                    'wjccs': len(tsTable.objects.filter(zt='未借出')),
                }
            )
        context['msg'] = ''
        context['smzt'] = smzt
        return render(request, 'dz_smztcx.html', context=context)


def dz_yydj(request):  # 读者预约登记(借不到的书)
    if request.session.get('login_type', None) != 'dz':
        return HttpResponseRedirect("/")
    context = dict()
    context['xm'] = request.session.get('xm', None)
    yydj = []
    result = yyTable.objects.filter(dzid_id=request.session.get('id', None))
    for elem in result:
        yydj.append(
            {
                'ISBN': elem.isbn.isbn,
                'sm': smTable.objects.get(isbn=elem.isbn.isbn).sm,
                'yysj': elem.yysj,
            }
        )
    context['yydj'] = yydj
    if request.method == 'GET':
        return render(request, 'dz_yydj.html', context=context)
    elif request.method == 'POST':
        context['msg'] = "未知错误，请重试"
        context['ISBN'] = isbn = request.POST.get('ISBN')
        if not isbn:
            context['msg'] = "请填写ISBN号进行预约登记"
            return render(request, 'dz_yydj.html', context=context)
        result = smTable.objects.filter(isbn=isbn)
        if not result.exists():
            context['msg'] = "ISBN输入有误，请重试"
            return render(request, 'dz_yydj.html', context=context)
        result = tsTable.objects.filter(isbn=isbn, zt='未借出')
        if result.exists():
            context['msg'] = "该书仍有馆藏，可以直接借阅(图书id：" + result[0].tsid + ")"
            return render(request, 'dz_yydj.html', context=context)
        result = yyTable.objects.filter(isbn=isbn, dzid=request.session.get('id', None))
        if result.exists():
            context['msg'] = "您已预约该书，请勿重复预约！"
            return render(request, 'dz_yydj.html', context=context)
        item = yyTable(
            dzid_id=request.session.get('id', None),
            isbn=smTable.objects.get(isbn=isbn),
            yysj=timezone.now()
        )
        item.save()
        context['msg'] = "预约成功！预约凭证已发送至您的邮箱！"
        mail(
            "预约成功通知函",
            "您已成功预约一本书, 书名为《" + str(smTable.objects.get(isbn=isbn).sm) +
            "》。预约时间：" + str(timezone.now())
        )
        yydj = []
        result = yyTable.objects.filter(dzid_id=request.session.get('id', None))
        for elem in result:
            yydj.append(
                {
                    'ISBN': elem.isbn.isbn,
                    'sm': smTable.objects.get(isbn=elem.isbn.isbn).sm,
                    'yysj': elem.yysj,
                }
            )
        context['yydj'] = yydj
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
    if request.method == 'GET':
        return render(request, 'gly_index.html', context=context)
    else:
        result = yyTable.objects.extra(where=["""datediff(curdate(), yysj) > 10"""])
        for elem in result:
            mail(
                "预约过期通知",
                "很遗憾，您预约的书《" + str(smTable.objects.get(isbn=elem.isbn.isbn).sm) + "》预约时间已经过期，您可以再次尝试预约"
            )
        context['msg'] = "已经清理" + str(len(result)) + "份过期预约信息"
        result.delete()
        return render(request, 'gly_index.html', context=context)


def gly_smztcx(request):  # 管理员书目状态查询
    if request.session.get('login_type', None) != 'gly':
        return HttpResponseRedirect("/")
    context = dict()
    context['xm'] = request.session.get('xm', None)
    if request.method == 'GET':
        return render(request, 'gly_smztcx.html', context=context)
    else:
        context['sm'] = sm = request.POST.get('sm')  # 书名
        context['zz'] = zz = request.POST.get('zz')  # 作者
        context['ISBN'] = isbn = request.POST.get('ISBN')  # ISBN
        context['cbs'] = cbs = request.POST.get('cbs')  # 出版社
        context['msg'] = "未知错误，请重试"
        result = smTable.objects.all()
        if not sm and not zz and not isbn and not cbs:
            context['msg'] = "请输入有效筛选信息！"
            return render(request, 'gly_smztcx.html', context=context)
        if sm:
            result = result.filter(sm__contains=sm)
        if zz:
            result = result.filter(zz__contains=zz)
        if isbn:
            result = result.filter(isbn__startswith=isbn)
        if cbs:
            result = result.filter(cbs__contains=cbs)
        smzt = []
        for elem in result:
            smzt.append(
                {
                    'ISBN': elem.isbn,
                    'sm': elem.sm,
                    'zz': elem.zz,
                    'cbs': elem.cbs,
                    'cbny': elem.cbny,
                    'kccs': len(tsTable.objects.filter(isbn=elem.isbn)),
                    'bwjcs': len(tsTable.objects.filter(zt='不外借')),
                    'wjccs': len(tsTable.objects.filter(zt='未借出')),
                }
            )
        context['msg'] = ''
        context['smzt'] = smzt
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
