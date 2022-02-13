from django.contrib import admin
from apps.blog.models import *

admin.site.site_header = 'zic博客管理系统'  # 设置header
admin.site.site_title = '大哥请放过'  # 设置title

# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)

admin.site.register(Sidebar)

"""

    title = models.CharField(max_length=64, verbose_name='文章标题')
    desc = models.TextField(max_length=256, blank=True, default='', verbose_name='文章描述')
    content = models.TextField(verbose_name='文章详情 ')
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=True, verbose_name='文章标签')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='种类')
    is_hot = models.BooleanField(default=0, verbose_name='是否成为热门') #手动热门
    pageview = models.IntegerField(default=0, verbose_name='浏览量')

"""


class ArticleAdmin(admin.ModelAdmin):
    '''文章详情'''
    list_display = ('title', 'tags', 'owner', 'category', 'is_hot', 'pageview', 'create_time')
    list_filter = ('owner',)
    search_fields = ('title', 'desc')
    list_editable = ('is_hot',)
    list_display_links = ('title', 'tags', 'owner', 'category', 'pageview', 'create_time')


admin.site.register(Article, ArticleAdmin)
