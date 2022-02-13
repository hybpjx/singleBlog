from django.urls import path, re_path
from apps.other.views import *

urlpatterns = [
    path('words/', WordsView.as_view(), name='words'),
    path('bug/', BugView.as_view(), name='bug')
]
