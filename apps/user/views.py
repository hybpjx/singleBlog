import time

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import login, authenticate, logout
from apps.user.forms import *
from apps.user.models import EmailVerifyCode, UserProfile
from utils.send_code import send_register
from django.contrib.auth.decorators import login_required


class RegisterView(View):
    def get(self, request):
        form = RegisterFrom()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = RegisterFrom(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get('password'))
            new_user.username = form.cleaned_data.get('email')
            # 发送邮件
            send_register(email=form.cleaned_data.get('email'), send_type='register')

            new_user.save()
            return HttpResponse('邮件已经发送，请注意查收')
        return render(request, 'user/register.html', {'form': form})


class ActiveView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyCode.objects.filter(code=active_code)
        if all_records:
            for records in all_records:
                email = records.email
                user = User.objects.get(email=email)
                user.is_staff = True
                user.save()

        else:
            return HttpResponse('链接有误')

        return redirect(reverse('user:login'))


class MyBackend(ModelBackend):
    """ 邮箱登录注册 """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):  # 加密明文密码
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        form = LoginFrom()
        return render(request, template_name='user/login.html', context={'form': form})

    def post(self, request):
        # username = request.POST['username']
        # password = request.POST['password']

        # if not all([username, password]):
        #     return render(request, 'user/login.html', {'errmsg': '数据不完整'})

        form = LoginFrom(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('user:profile'))
            else:
                return HttpResponse('登录失败')

        context = {'form': form}
        return render(request, 'user/login.html', context)


class ForgetPwdView(View):
    def get(self, request):
        form = ForgetPwdForm()
        return render(request, 'user/forget_pwd.html', {'form': form})

    def post(self, request):
        form = ForgetPwdForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            is_exists = User.objects.filter(email=email).exists()
            if is_exists:
                send_register(email, 'forget')
                return HttpResponse('邮件已经发送，请注意查收')
            else:
                return HttpResponse('邮箱可能暂未注册，请先注册')

        return render(request, 'user/forget_pwd.html', {'form': form})


class ModifyPwdView(View):
    def get(self, request, **kwargs):
        form = ModifyPwdForm()
        return render(request, 'user/modify_pwd.html', {'form': form})

    def post(self, request, active_code):
        form = ModifyPwdForm(request.POST)
        if form.is_valid():
            records = EmailVerifyCode.objects.get(code=active_code)
            email = records.email
            user = User.objects.get(email=email)
            user.username = email
            user.password = make_password(form.cleaned_data.get('password'))
            user.save()
            return HttpResponse('修改成功')
        else:
            return HttpResponse('步骤出错，密码修改失败')


class UserProfileView(View):
    @method_decorator(login_required(login_url='/user/login/'))
    def get(self, request):
        user = request.user
        return render(request, 'user/user_profile.html', {'user': user})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('user:login'))


class EditorUserView(View):
    @method_decorator(login_required(login_url='/user/login/'))
    def get(self, request):
        user = UserProfile.objects.get(owner_id=request.user.id)

        return render(request, "user/editor_user.html", {'user': user})

    @method_decorator(login_required(login_url='/user/login/'))
    def post(self, request):
        nick_name = request.POST["nickName"]
        desc = request.POST["desc"]
        signature = request.POST["signature"]
        birth = request.POST["birth"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        # avatar = request.FILES.get("avatar")
        # print(nick_name,desc,signature,birth,gender,address,avatar)
        # if not all([nick_name, desc, signature, birth, gender, address, avatar]):
        #     # 数据不完整
        #     return render(request, 'user/editor_user.html', {'errmsg': '数据不完整'})

        try:
            user = UserProfile.objects.get(nickname=nick_name)

        except UserProfile.DoesNotExist:
            user = None

        if user:
            # 用户名已存在
            return render(request, 'user/editor_user.html', {'errmsg': '昵称已存在'})
        try:
            UserProfile.objects.filter(owner_id=request.user.id).update(
                nickname=nick_name,
                desc=desc,
                # avatar=avatar,
                signature=signature,
                gender=gender,
                address=address,
                birth=birth
            )
        except Exception as e:
            return render(request, 'user/editor_user.html', {'errmsg': '对不起 均是必填项 如若不修改 请返回'})
        return render(request, "user/user_profile.html")



# @login_required(login_url="user:login")
# def editor_users(request):
#     user = User.objects.get(id=request.user.id)
#     if request.method == "POST":
#         try:
#             user_profile = user.userprofile
#             form = UserForm(request.POST, instance=user)  # 填充 默认数据 为当前用户
#             user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)  # 填充默认数据
#             print(1)
#             if form.is_valid() and user_profile_form.is_valid():
#                 form.save()
#                 user_profile_form.save()
#                 return redirect('user:profile')
#
#         except UserProfile.DoesNotExist:  # 这里发生错误 说明 userprofile 无数据
#             form = UserForm(request.POST, instance=user)
#             user_profile_form = UserProfileForm(request.POST, request.FILES)  # 填充默认数据 直接获取 表单数据 空数据 保存
#             print(user_profile_form)
#             if form.is_valid() and user_profile_form.is_valid():
#                 form.save()
#                 # user_profile_form.save()
#                 print("KJLJLKJLJLK")
#                 # commit = False 等于先不保存  把数据先放入内存中 ，然后在重新给指定的字段 赋值添加进去,提交保存新的数据
#                 new_user_profile_form = user_profile_form.save(commit=False)
#                 new_user_profile_form.owner = user
#                 new_user_profile_form.save()
#                 return redirect('user:profile')
#
#     else:
#         try:
#             user_profile = user.userprofile
#             userprofile = user.userprofile
#             form = UserForm(instance=user)
#             user_profile_form = UserProfileForm(instance=userprofile)
#         except UserProfile.DoesNotExist:
#             form = UserForm(instance=user)
#             user_profile_form = UserProfileForm()  # 显示空表单
#         return render(request, 'user/editor_user.html', locals())
#     return render(request, 'user/user_profile.html')
