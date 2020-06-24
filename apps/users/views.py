import redis
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View

from MxOnline.settings import yp_apikey, REDIS_HOST, REDIS_PORT
from apps.operations.models import UserProfile
from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm, RegisterPostForm, \
    UploadImageForm
from apps.utils.YunPian import send_single_sms
from apps.utils.random_str import generate_random


# 基于CBV模式开发
class UploadImageView(LoginRequiredMixin, View):
    login_url = "/login/"

    # def save_file(self, file):
    #     with open("", "wb") as f:
    #         for chunk in file.chunks():
    #             f.write(chunk)

    def post(self, request, *args, **kwargs):
        # 处理用户上传的头像
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })

        # files = request.FILES['image']
        # self.save_file(files)

        # 1. 如果同一个文件上传多次，相同名称的文件应该如何处理


class UserInfoView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        return render(request, "usercenter-info.html")


class RegisterView(View):
    """注册"""

    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()

        return render(request, "register.html", {"register_get_form": register_get_form})

    def post(self, request, *args, **kwargs):
        register_post_form = RegisterPostForm(request.POST)
        if register_post_form.is_valid():
            # 没有注册账号依然可以登录
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]
            # 新建一个游客用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            register_get_form = RegisterGetForm()
            return render(request, "register.html",
                          {"register_get_form": register_get_form, "register_post_form": register_post_form})


class DynamicLoginView(View):
    """
    验证码动态登录
    """

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()
        return render(request, "login.html", {
            "login_form": login_form,
            "next": next
        })

    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        if login_form.is_valid():
            # 没有注册账号依然可以登录
            mobile = login_form.cleaned_data["mobile"]
            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                # 新建一个游客用户
                user = UserProfile(username=mobile)
                password = generate_random(10, 2)
                user.set_password(password)
                user.mobile = mobile
                user.save()
            login(request, user)

            next = request.GET.get("next", "")
            if next:
                return HttpResponseRedirect(next)

            return HttpResponseRedirect(reverse("index"))
        else:
            d_form = DynamicLoginForm()
            return render(request, "login.html", {"login.html": login_form, "d_form": d_form})


class SendSmsView(View):
    """
    发送短信
    """

    def post(self, request, *args, **kwargs):
        send_sms_form = DynamicLoginForm(request.POST)
        re_dict = {}
        if send_sms_form.is_valid():
            mobile = send_sms_form.cleaned_data["mobile"]
            # 随机生成数字验证码
            code = generate_random(4, 0)

            re_json = send_single_sms(yp_apikey, code, mobile=mobile)
            if re_json["code"] == 0:
                re_dict["status"] = "success"
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
                r.set(str(mobile), code)
                r.expire(str(mobile), 300)  # 设置验证码5分钟过期
            else:
                re_dict["msg"] = re_json["msg"]

        else:
            for key, value in send_sms_form.errors.items():
                re_dict[key] = value[0]
            return JsonResponse(re_dict)


class LogoutView(View):
    """
    退出登录
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

        # 登录成功之后返回原页面
        next = request.GET.get("next", "")

        login_form = DynamicLoginForm(request.POST)

        return render(request, "login.html", {
            "login_form": login_form,
            "next": next
        })

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

                # 登录成功之后返回原页面
                next = request.GET.get("next", "")
                if next:
                    return HttpResponseRedirect(next)

                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误", "login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})
