#  在这里自定义模版标签
from django import template
from apps.blog.models import *

register = template.Library()


@register.simple_tag
def get_category_list():
    return Category.objects.all()


@register.simple_tag
def get_sidebar_list():
    return Sidebar.get_sidebar()


@register.simple_tag
def get_new_list():
    # 查询最新数据
    return Article.objects.order_by('-create_time')[:8]


@register.simple_tag
def get_hot_list():
    # 查询热门文章1
    return Article.objects.filter(is_hot=True)[:5]


# @register.simple_tag
# def get_hot_pageview_list():
#     # 查询热门文章2
#     return Article.objects.order_by('-pageview')[:8]


@register.simple_tag
def get_archives():
    return Article.objects.dates('create_time', 'month', order='DESC')[:8]


