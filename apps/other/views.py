from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.views import View

from apps.other.models import BugSubmit, HelpSubmit


class WordsView(View):
    def get(self, request):
        word_list = HelpSubmit.objects.all()
        user = request.user

        paginator = Paginator(word_list, 5)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)

        context = {
            'word_list': word_list,
            'user':user,
            'page_obj': page_obj
            }
        return render(request, 'other/words.html',context)

    def post(self, request):
        textarea = request.POST['text_area']
        if not textarea:
            return render(request, 'other/words.html', {'errmgs': '不能添加空值'})
        word = HelpSubmit()
        word.words = textarea
        word.save()

        user =request.user

        word_list = HelpSubmit.objects.all()

        paginator = Paginator(word_list, 5)
        page_num = request.GET.get('page')
        page_obj = paginator.get_page(page_num)

        context = {
            'word_list': word_list,
            'user':user,
            'page_obj': page_obj
            }

        if word_list:
            return render(request, 'other/words.html', context)
        else:
            return render(request, 'other/words.html', {'errmgs': '添加失败'})


class BugView(View):
    def get(self, request):
        return render(request, 'other/bug.html')

    def post(self, request):
        name = request.POST['name']
        email = request.POST['email']
        textarea = request.POST['text_area']
        checked = request.POST['checked']

        if not all([name, email, textarea]):
            return render(request, 'other/bug.html', {'errmsg': '请您完整填写信息'})

        if checked == "off":
            return render(request, 'other/bug.html', {'errmsg': '请您同意条约'})

        bug = BugSubmit()
        bug.name = name
        bug.email = email
        bug.bug = textarea
        bug.save()

        return render(request, 'other/bug.html', {'errmsg': '完成提交'})
