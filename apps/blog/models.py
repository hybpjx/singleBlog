from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string

from db.basemodel import BaseModel
from ckeditor.fields import RichTextField


# Create your models here.


class Category(BaseModel):
    '''分类种类'''
    name = models.CharField(max_length=32, verbose_name='分类名称')
    desc = models.CharField(max_length=32, blank=True, default='', verbose_name='分类简介')

    class Meta:
        verbose_name = '博客分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(BaseModel):
    '''文章标签'''
    name = models.CharField(max_length=32, verbose_name='文章标签')

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(BaseModel):
    '''文章模型'''
    title = models.CharField(max_length=64, verbose_name='文章标题')
    desc = models.TextField(max_length=256, blank=True, default='', verbose_name='文章描述')
    content = RichTextField(verbose_name='文章详情 ')
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=True, verbose_name='文章标签')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='种类')
    is_hot = models.BooleanField(default=0, verbose_name='是否成为热门') #手动热门
    pageview = models.IntegerField(default=0, verbose_name='浏览量')

    class Meta:
        verbose_name = '文章内容'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Sidebar(BaseModel):
    '''侧边栏模型数据'''
    DISPLAY_TYPE = (
        (1, '搜索'),
        (2, '最新文章'),
        (3, '热门文章'),
        (4, '最近评论'),
        (5, '文件归档'),
        (6, 'HTML'),

    )

    STATUS = (
        (1, '隐藏'),
        (2, '展示'),
    )

    title = models.CharField(max_length=64, verbose_name='模块名称')
    display_type = models.PositiveIntegerField(default=1, choices=DISPLAY_TYPE, verbose_name='展示类型')
    content = models.TextField(blank=True, default='', verbose_name='内容', help_text='如果不是HTML类型的，可为空')
    sort = models.PositiveIntegerField(default=1, verbose_name='排序', help_text='排序')
    status = models.PositiveIntegerField(default=2, choices=STATUS, verbose_name='状态')

    class Meta:
        verbose_name = '侧边栏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    @classmethod
    def get_sidebar(cls):
        return cls.objects.filter(status=2)

    @property
    def get_content(self):
        if self.display_type == 1:
            context = {

            }
            return render_to_string('blog/sidebar/search.html', context=context)

        elif self.display_type == 2:
            context = {

            }

            return render_to_string('blog/sidebar/new.html', context=context)

        elif self.display_type == 3:
            context = {

            }

            return render_to_string('blog/sidebar/hot.html', context=context)

        elif self.display_type == 4:
            context = {

            }

            return render_to_string('blog/sidebar/comment.html', context=context)

        elif self.display_type == 5:
            context = {

            }

            return render_to_string('blog/sidebar/archives.html', context=context)

        elif self.display_type == 6:
            '''自定义侧边栏'''
            return self.content  # 直接返回content




# class Comment(BaseModel):
#     article = models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name='评论文章')
#     user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='评论者')
#     content = models.CharField(verbose_name='评论内容', max_length=255)