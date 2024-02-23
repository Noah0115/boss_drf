from django.db import models
from django.contrib.auth.models import User, AbstractUser


class UserInfo(models.Model):
    """
        back_userinfo
        用户表
    """
    username = models.CharField(verbose_name='用户名', max_length=32, null=True, blank=False, unique=True)
    password = models.CharField(verbose_name='密码', max_length=16, null=True, blank=False)
    email = models.CharField(verbose_name='邮箱', null=True, max_length=64, unique=True)
    phone = models.CharField(verbose_name='手机号', max_length=64, null=True, blank=False, unique=True)
    qq = models.CharField(verbose_name='QQ号', null=True, blank=True, default='', max_length=20)
    wechat = models.CharField(verbose_name='微信号', max_length=64, blank=True, null=True, default='')
    address = models.CharField(verbose_name='收货地址', null=True, blank=True, max_length=64, default='')
    work = models.CharField(verbose_name='工作单位', null=True, blank=True, max_length=64, default='')
    role = models.IntegerField(verbose_name='角色', default=0)
    introduction = models.TextField(verbose_name='个人简介', null=True, blank=True, default='这个人很懒，不爱写简介',
                                    max_length=300)
    pic = models.CharField(verbose_name='头像', max_length=300, default='/static/user_default.png')
    status = models.IntegerField(verbose_name='账号状态', default=1)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    last_time = models.DateTimeField(verbose_name='最后登录时间', auto_now=True)


class Admin(models.Model):
    """
        back_admin
        管理员表
    """
    admin_name = models.CharField(verbose_name='管理员名称', max_length=32, null=True, blank=False)
    admin_password = models.CharField(verbose_name='管理员密码', max_length=32, null=True, blank=False)
    role = models.IntegerField(verbose_name='角色', default=1)
    status = models.IntegerField(verbose_name='账号状态', default=1)
    groupid = models.IntegerField(verbose_name='组ID', default=1)

class Jobinfo(models.Model):
    """
        back_Jobinfo
        招聘工作信息表
    """
    job_title = models.CharField(verbose_name='工作名称', max_length=200, null=True, blank=False)
    job_area = models.CharField(verbose_name='工作地点', max_length=200, null=True, blank=False)
    salary_bot = models.CharField(verbose_name='最低薪资', max_length=200, null=True, blank=False)
    salary_top = models.CharField(verbose_name='最高薪资', max_length=200, null=True, blank=False)
    year = models.CharField(verbose_name='工作经验年限', max_length=200, null=True, blank=False)
    education = models.CharField(verbose_name='受教育水平', max_length=200, null=True, blank=False)
    company_title = models.CharField(verbose_name='公司名称', max_length=200, null=True, blank=False)
    company_info = models.CharField(verbose_name='公司规模', max_length=200, null=True, blank=False)
    skill = models.CharField(verbose_name='技能要求', max_length=200, null=True, blank=False)
    publis_name = models.CharField(verbose_name='发布者', max_length=200, null=True, blank=False)
    welfare = models.CharField(verbose_name='福利待遇', max_length=200, null=True, blank=False)
    type = models.CharField(verbose_name='职业类型', max_length=200, null=True, blank=False)



