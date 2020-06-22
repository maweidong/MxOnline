import redis
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View

from MxOnline.settings import yp_apikey, REDIS_HOST, REDIS_PORT
from apps.users.forms import LoginForm, DynamicLoginForm
from apps.utils.YunPian import send_single_sms
from apps.utils.random_str import generate_random


# 基于CBV模式开发

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

        login_form = DynamicLoginForm(request.POST)

        return render(request, "login.html", {
            "login_form": login_form
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

                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误", "login_form": login_form})
        else:
            return render(request, "login.html", {"login_form": login_form})
