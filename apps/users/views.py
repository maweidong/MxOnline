from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.


# 基于CBV模式开发
from django.urls import reverse
from django.views.generic.base import View

from apps.users.forms import LoginForm


class LogoutView(View):
    """
    退出
    """

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


class LoginView(View):
    """
    登录
    """

    def get(self, request, *args, **kwargs):
        # 判断用户是否登录
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        return render(request, "login.html")

    def post(self, request, *args, **kwargs):
        # 表单验证
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 用于通过用户名和密码查询用户是否存在
            user_name = login_form.cleaned_data["username"]  # 获取form处理后的数据
            password = login_form.cleaned_data["password"]

            user = authenticate(username=user_name, password=password)

            if user is not None:
                # django自带login方法，自动设置sessionid
                login(request, user)

                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误", "login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})
