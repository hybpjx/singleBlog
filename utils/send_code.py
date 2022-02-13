import random, string
from django.core.mail import send_mail
from apps.user.models import EmailVerifyCode
from singleBlog import settings


def verify_code():
    '''生成的8位'''
    random_length = 8
    # a-z A-Z 0-9
    str_code = string.ascii_letters + string.digits
    # 生成的随机8位字符串
    code = ''.join(random.sample(str_code, random_length))
    return code


def send_register(email, send_type='register'):
    # send_type = 'register'
    email_code = EmailVerifyCode()
    code = verify_code()
    email_code.code = code
    email_code.email = email
    email_code.send_type = send_type
    email_code.save()

    if send_type == 'register':
        # subject, message, from_email, recipient_list,
        #               fail_silently=False, auth_user=None, auth_password=None,
        #               connection=None, html_message=None
        subject = 'zic博客欢迎你成为注册用户'
        message = ''
        html_message = '<h1>你好，%s 欢迎您成为zic博客注册用户</h1><div>请点击一下链接激活账号：</div> <a href="http://l4284698l9.zicp.vip/user/active/%s">http://l4284698l9.zicp.vip/user/active/%s</a>' % (email, code, code)
        sender = settings.EMAIL_FROM
        reciver = [email]
        send_mail(subject, message, sender, reciver,html_message=html_message)

    elif send_type == 'forget':
        # subject, message, from_email, recipient_list,
        #               fail_silently=False, auth_user=None, auth_password=None,
        #               connection=None, html_message=None
        subject = '找回密码'
        message = ''
        html_message = '<h1>你好，%s 欢迎您成为zic博客注册用户</h1><div>请点击一下链接找回密码：</div> <a href="http://l4284698l9.zicp.vip/user/modify_pwd/%s">http://l4284698l9.zicp.vip/user/modify_pwd/%s</a>' % (email, code, code)
        sender = settings.EMAIL_FROM
        reciver = [email]
        send_mail(subject, message, sender, reciver, html_message=html_message)
