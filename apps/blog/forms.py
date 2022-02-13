from django import forms
from django.forms.widgets import *
from apps.blog.models import *


class PublicContext(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['title', 'desc','content', 'tags', 'category',]
        widgets = {
            'title': TextInput(attrs={
                'class': 'input',
                "placeholder": '标题'
            }),
            'desc': Textarea(attrs={
                'class': 'input',
                "placeholder": '简介'
            }),

            'tags': Select(attrs={
                'class': 'select',
                "placeholder": '标签'
            }),


            'category': Select(attrs={
                'class': 'input button',
                "placeholder": '种类'
            }),

        }

