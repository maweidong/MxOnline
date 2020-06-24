import redis
from django import forms
from captcha.fields import CaptchaField

from MxOnline.settings import REDIS_HOST, REDIS_PORT
from apps.operations.models import UserProfile


class UploadImageForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ["image"]


class RegisterGetForm(forms.Form):
    # 获取图片验证码
    captcha = CaptchaField()


class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)
    password = forms.CharField(required=True)

    def clean_mobile(self):
        mobile = self.data.get("mobile")
        # 验证手机号码是否已注册
        users = UserProfile.objects.filter(mobile=mobile)
        if users:
            raise forms.ValidationError("该手机号码已注册")

        return mobile

    # 用clean_加字段名方式验证code字段是否正确
    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))

        if code != redis_code:
            raise forms.ValidationError("验证码不正确")

        # 验证手机号码是否已注册
        users = UserProfile.objects.filter(mobile=mobile)
        if users:
            raise forms.ValidationError("改手机号码已注册")

        return code


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=2)
    password = forms.CharField(required=True, max_length=3)


class DynamicLoginForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    captcha = CaptchaField()


class DynamicLoginPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    # 用clean_加字段名方式验证code字段是否正确
    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))

        if code != redis_code:
            raise forms.ValidationError("验证码不正确")

        return self.cleaned_data

    # # 重写clean方法，验证code是否正确
    # def clean(self):
    #     mobile = self.cleaned_data["mobile"]
    #     code = self.cleaned_data["code"]
    #
    #     r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
    #     redis_code = r.get(str(mobile))
    #
    #     if code != redis_code:
    #         raise forms.ValidationError("验证码不正确")
    #
    #     return self.cleaned_data
