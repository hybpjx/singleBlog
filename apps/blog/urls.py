from django.contrib.auth.decorators import login_required
from django.urls import path, re_path

from apps.blog import views
from apps.blog.views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('category/<int:category_id>/', CategoryView.as_view(), name='category_list'),
    path('article/<int:article_id>/', ArticleDetailView.as_view(), name='article_detail'),
    path('archives/<int:year>/<int:month>/', ArchivesView.as_view(), name='archives'),
    path('public/', PublicView.as_view(), name='public'),
]
