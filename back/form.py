from django import forms
from back import models
from django.forms import widgets
from back.utils import Bootstarp
from django.core.exceptions import ValidationError
import re


def email_validate(value):  # 定义一个邮箱格式匹配函数
    email_re = re.compile(r'^.*?@qq\.com$')  # 非贪婪匹配
    if not email_re.match(value):
        raise ValidationError('邮箱格式错误')


class LoginModelForm(Bootstarp.BootstarpForm):
    class Meta:
        model = models.UserInfo
        fields = ['phone', 'password']
        widgets = {
            "phone": widgets.TextInput({"class": "form-control", "id": "yourphone"}),
            "password": widgets.TextInput({"class": "form-control", "type": "password", "id": "yourpassword"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # for name, field in self.fields.items():
        #     print(name)


class RegisterModelForm(Bootstarp.BootstarpForm):
    class Meta:
        model = models.UserInfo
        fields = ['phone', 'email', 'password']
        widgets = {
            "phone": widgets.TextInput({"class": "form-control", "id": "yourphone"}),
            "email": widgets.TextInput({"class": "form-control", "id": "youremail"}),
            "password": widgets.TextInput({"class": "form-control", "type": "password", "id": "yourpassword"}),
        }
        error_messages = {
            "phone": {"required": "用户名不能包含*/-+.等特殊符号"},
            "email": {"required": "邮箱格式不正确"},
            "password": {"required": "密码必须大于8位"}
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class ChangeProfileModelForm(Bootstarp.BootstarpForm):
    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'phone', 'qq', 'wechat', 'address', 'work', 'introduction']
        widgets = {
            "username": widgets.TextInput(
                {"class": "form-control", "id": "username", "type": "text", "readonly": "readonly"}),
            "email": widgets.TextInput(
                {"class": "form-control", "id": "email", "type": "text", "readonly": "readonly"}),
            "phone": widgets.TextInput(
                {"class": "form-control", "id": "phone", "type": "text", "readonly": "readonly"}),
            "qq": widgets.TextInput({"class": "form-control", "id": "qq", "type": "text"}),
            "wechat": widgets.TextInput({"class": "form-control", "id": "wechat", "type": "text"}),
            "address": widgets.TextInput({"class": "form-control", "id": "address", "type": "text"}),
            "work": widgets.TextInput({"class": "form-control", "id": "work", "type": "text"}),
            "introduction": widgets.Textarea({"class": "form-control", "id": "introduction", "type": "text"})
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class UserForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['username', 'password','email', 'phone', 'qq', 'wechat', 'address', 'work', 'introduction', 'role']
        widgets = {
            "username": widgets.TextInput({"class": "layui-input", "id": "username", "type": "text"}),
            "password": widgets.TextInput({"class": "layui-input", "id": "password", "name": "password", "type": "password"}),
            "email": widgets.TextInput({"class": "layui-input", "id": "email", "type": "text"}),
            "phone": widgets.TextInput({"class": "layui-input", "id": "phone", "type": "text"}),
            "qq": widgets.TextInput({"class": "layui-input", "id": "qq", "type": "text"}),
            "wechat": widgets.TextInput({"class": "layui-input", "id": "wechat", "type": "text"}),
            "address": widgets.TextInput({"class": "layui-input", "id": "address", "type": "text"}),
            "work": widgets.TextInput({"class": "layui-input", "id": "work", "type": "text"}),
            "introduction": widgets.Textarea({"class": "layui-input", "id": "introduction", "type": "text"}),
            "role": widgets.TextInput({"class": "layui-input", "id": "role", "type": "text"}),
        }
        error_messages = {
            "phone": {"unique": "手机号已存在"},
            "email": {"required": "邮箱格式不正确"},
            "password": {"required": "密码必须大于8位"}
        }
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class AdminForm(forms.ModelForm):
    class Meta:
        model = models.Admin
        fields = ['admin_name', 'admin_password', 'status', 'groupid', 'role']
        widgets = {
            "admin_name": widgets.TextInput(
                {"class": "layui-input", "id": "username", "name": "admin_name", "type": "username"}),
            "admin_password": widgets.TextInput(
                {"class": "layui-input", "id": "password", "name": "admin_password", "type": "password"}),
        }
        error_messages = {
            "admin_name": {"unique": "用户已存在"}
        }
