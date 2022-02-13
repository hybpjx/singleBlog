import extras
from django import forms
from django.contrib.auth.models import User
from django.forms import DateField
from django.forms.widgets import TextInput, FileInput, DateInput, CheckboxInput
from django.utils import timezone

from apps.user.models import UserProfile


class RegisterFrom(forms.ModelForm):
    email = forms.EmailField(label='邮箱', max_length=32, widget=forms.EmailInput(attrs={
        'class': 'input', 'placeholder': '邮箱'
    }))

    password = forms.CharField(label='密码', min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '密码'
    }))

    repeat_password = forms.CharField(label='再次输入密码', min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '再次输入密码'
    }))

    email = forms.CharField(label='请输入邮箱', max_length=32, widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder': '输入邮箱'
    }))

    class Meta:
        model = User
        fields = ('email', "password")

    def clean_email(self):
        '''
        用户是否存在
        :return:
        '''
        email = self.cleaned_data.get('email')
        is_exists = User.objects.filter(email=email).exists()
        if is_exists:
            raise forms.ValidationError('用户已存在')
        return email

    def clean_repeat_password(self):
        '''验证两次密码是否一致'''
        if self.cleaned_data['password'] != self.cleaned_data['repeat_password']:
            raise forms.ValidationError('两次密码不一致')

        return self.cleaned_data['repeat_password']


class LoginFrom(forms.Form):
    username = forms.CharField(label='用户名', max_length=32, widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))
    password = forms.CharField(label='密码', min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '密码'
    }))

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username == password:
            raise forms.ValidationError('用户名和密码尽量不要相同')
        return password


class ForgetPwdForm(forms.Form):
    email = forms.EmailField(label='请输入注册邮箱地址', min_length=4, widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))


class ModifyPwdForm(forms.Form):
    password = forms.CharField(label='输入新密码', min_length=8, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '输入新密码'
    }))


class UserForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'input', 'disabled': 'disabled'
    }))

    class Meta:
        model = User
        fields = ('email',)


# class UserProfileForm(forms.ModelForm):
#     """个人中心表单编辑"""
#
#     gender = forms.fields.ChoiceField(
#         choices=(("保密", "保密"), ("男", "男"), ("女", "女"),),
#         label="性别",
#         initial=3,
#         widget=forms.widgets.Select(),
#     )
#
#     birth = forms.fields.ChoiceField(
#         widget=forms.widgets.SelectDateWidget(),
#     )
#
#     class Meta:
#         model = UserProfile
#         fields = ('nickname', 'desc', 'signature', 'birth', 'gender', 'address', 'avatar')
#         birth = DateField(input_formats=['%d-%m-%Y'])
#         widgets = {
#             'nickname': TextInput(attrs={
#                 'class': 'input',
#                 "placeholder": '昵称'
#             }),
#             'desc': TextInput(attrs={
#                 'class': 'input',
#                 "placeholder": '简介'
#             }),
#             'signature': TextInput(attrs={
#                 'class': 'input',
#                 "placeholder": '签名'
#             }),
#             'address': TextInput(attrs={
#                 'class': 'input',
#                 "placeholder": '地址'
#             }),
#         }

class UserProfileForm(forms.ModelForm):
    """个人中心表单编辑"""
    class Meta:
        model = UserProfile
        fields = ('nickname', 'desc', 'signature', 'birth', 'gender', 'address', 'avatar')
