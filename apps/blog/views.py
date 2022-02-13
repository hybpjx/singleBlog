from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.shortcuts import render, get_object_or_404,HttpResponse

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View

from apps.blog.forms import PublicContext
from apps.blog.models import *


class IndexView(View):
    '''
    主页
    '''

    def get(self, request):
        # 所有文章
        keyword = request.GET.get('keyword')

        if keyword:
            article_list = Article.objects.filter(
                Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword))

            paginator = Paginator(article_list, 5)
            page_num = request.GET.get('page')
            page_obj = paginator.get_page(page_num)
            context = {'article_list': article_list,
                       'page_obj': page_obj
                       }

            return render(request, 'blog/index.html', context)
        else:
            article_list = Article.objects.all()
            paginator = Paginator(article_list, 5)
            page_num = request.GET.get('page')
            page_obj = paginator.get_page(page_num)
            context = {'article_list': article_list,
                       'page_obj': page_obj
                       }

            return render(request, 'blog/index.html', context)


class CategoryView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, id=category_id)
        article_list = category.article_set.all()

        paginator = Paginator(article_list, 5)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)
        context = {'category': category,
                   'article_list': article_list,
                   'page_obj':page_obj

                   }
        return render(request, 'blog/list.html', context)


class ArticleDetailView(View):
    '''详情页'''

    def get(self, request, article_id):
        article = get_object_or_404(Article, id=article_id)
        # 用文章id实现上一篇下一篇
        prev_article = Article.objects.filter(id__lt=article.id).last()
        next_article = Article.objects.filter(id__gt=article.id).first()
        Article.objects.filter(id=article.id).update(pageview=F('pageview') + 1)

        # # 用时间实现上一篇
        # prev_article = Article.objects.filter(create_time__lt=article.create_time).last()
        # next_article = Article.objects.filter(create_tim__gt=article.create_time).first()

        context = {
            'article': article,
            'prev': prev_article,
            'next': next_article,
        }

        return render(request, 'blog/detail.html', context)


class ArchivesView(View):
    def get(self, request, year, month):
        article_list = Article.objects.filter(create_time__year=year, create_time__month=month)
        # print(article_list)

        article_list = Article.objects.all()
        paginator = Paginator(article_list, 5)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)

        context = {'article_list': article_list, 'page_obj': page_obj, '' 'year': year, 'month': month}
        return render(request, 'blog/archives_list.html', context)


class PublicView(View):
    @method_decorator(login_required(login_url='/user/login/'))
    def get(self, request):

        category = Category.objects.all()
        form = PublicContext()

        context = {
            'category': category,
            'form':form
        }

        return render(request, 'blog/public.html', context)

    @method_decorator(login_required(login_url='/user/login/'))
    def post(self,request):
        form = PublicContext(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            content = form.cleaned_data.get('content')
            tags = form.cleaned_data.get('tags')
            category = form.cleaned_data.get('category')
            user = request.user

            article = Article()
            article.title= title
            article.desc = desc
            article.content = content
            article.tags = tags
            article.category = category
            article.owner = user
            article.save()
            return render(request,'blog/public.html',{'errmsg':'添加成功'})

        return render(request,'blog/public.html',{'errmsg':'请正常操作'})