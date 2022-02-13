from django.db import models
from django.contrib.auth.models import User
from db.basemodel import BaseModel


# Create your models here.


# 用户配置中心
class UserProfile(BaseModel):
    USER_GENDER_TYPE = (
        ('secrecy', '保密'),
        ('male', '男'),
        ('female', '女')
    )

    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户',auto_created=True)
    nickname = models.CharField(max_length=16, blank=True, verbose_name='昵称')
    desc = models.TextField(max_length=254, blank=True, default='', verbose_name='个人简介')
    signature = models.CharField(max_length=64, blank=True, default='', verbose_name='个性签名')
    birth = models.DateField(null=True, blank=True, verbose_name='出生日期')
    gender = models.CharField(max_length=8, choices=USER_GENDER_TYPE, default='secrecy', verbose_name='性别')
    address = models.CharField(max_length=96, blank=True, default='', verbose_name='地址')
    avatar = models.ImageField(upload_to='images/%Y/%m',blank=True,null=True, default='images/default.jpg', max_length=100,
                               verbose_name='用户头像')

    class Meta:
        verbose_name = '用户配置中心'
        verbose_name_plural = '用户配置中心'

    def __str__(self):
        return self.owner.username


class EmailVerifyCode(BaseModel):
    '''邮箱验证码'''
    SEND_TYPE_CHOICES= {
        ('register', '注册'),
        ('forget', '找回密码')
    }

    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=35, verbose_name='邮箱')
    send_type = models.CharField(choices=SEND_TYPE_CHOICES, default='register', max_length=16, verbose_name='验证种类')

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = '邮箱验证码'

    def __str__(self):
        return self.code