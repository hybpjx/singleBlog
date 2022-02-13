from django.contrib.auth.decorators import login_required
from django.urls import path, re_path
from apps.user.views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    re_path(r'^active/(?P<active_code>.*)$', ActiveView.as_view(), name='active'),
    path('forget_pwd/', ForgetPwdView.as_view(), name='forget_pwd'),
    re_path(r'^modify_pwd/(?P<active_code>.*)$', ModifyPwdView.as_view(), name='modify_pwd'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('editor_user/', EditorUserView.as_view(),name='editor')
    # path('editor_user/', editor_users, name='editor')
]


