"""Library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myWEB import views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),

    path('login_view/', views.login_view),  # 登录
    path('register/', views.register),  # 注册
    path('logout_view/', views.logout_view),  # 退出登录

    path('dz_index/', views.dz_index),  # 读者首页
    path('dz_smztcx/', views.dz_smztcx),  # 读者书目状态查询
    path('dz_yydj/', views.dz_yydj),  # 读者预约登记
    path('dz_grztcx/', views.dz_grztcx),  # 读者个人状态查询

    path('gly_index/', views.gly_index),  # 管理员首页
    path('gly_smztcx/', views.gly_smztcx),  # 读者书目状态查询
    path('gly_js/', views.gly_js),  # 管理员借书
    path('gly_hs/', views.gly_hs),  # 管理员还书
    path('gly_rk/', views.gly_rk),  # 管理员入库
    path('gly_ck/', views.gly_ck),  # 管理员出库


]
